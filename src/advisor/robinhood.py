import os
from dotenv import load_dotenv
import robin_stocks.robinhood as r
from advisor.allocate import get_stock_allocations, get_stock_lists

load_dotenv(".env")

def login():
    r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))

def get_positions():
    login()
    return r.build_holdings()

def print_positions():
    for ticker, data in get_positions().items():
        print(f"Stock: {ticker}")
        print(f"Quantity: {data['quantity']}")
        print(f"Average Buy Price: ${data['average_buy_price']}")
        print(f"Current Price: ${data['price']}")
        print(f"Total Equity: ${data['equity']}")
        print("---")

def get_current_prices(tickers):
    return {ticker: float(r.stocks.get_latest_price(ticker)[0]) for ticker in tickers}


def compare_allocations_to_positions():
    login()  # Ensure we're logged in
    allocations = get_stock_allocations()
    positions = get_positions()

    all_tickers = set(allocations.keys()) | set(positions.keys())
    current_prices = get_current_prices(all_tickers)

    comparison = {}

    for ticker in all_tickers:
        allocated_amount = allocations.get(ticker, 0)
        current_equity = float(positions.get(ticker, {}).get('equity', 0))
        price = current_prices[ticker]
        owned = ticker in positions

        if current_equity == 0:
            difference = allocated_amount  # For stocks we don't own, difference is the full allocated amount
        else:
            difference = allocated_amount - current_equity

        comparison[ticker] = {
            'difference': round(difference, 2),
            'price': price,
            'current_equity': current_equity,
            'owned': owned
        }

    return comparison

def allocate_new_investment():
    new_amount = float(os.getenv('NEW_AMOUNT', 0))
    comparison = compare_allocations_to_positions()
    stock_lists = get_stock_lists()

    # Flatten and prioritize stock lists
    priority_list = []
    for category in ['STRONG_BUY', 'BUY', 'MODERATE_BUY', 'ETF']:
        if category in stock_lists:
            priority_list.extend(stock_lists[category][0])

    # Debug: Print all stocks in comparison
    print("All stocks in comparison:")
    for ticker, data in comparison.items():
        print(f"{ticker}: {data}")

    # Stocks we don't own yet
    zero_position_stocks = [ticker for ticker, data in comparison.items() if not data['owned']]

    # Debug: Print zero position stocks
    print("\nZero position stocks:")
    print(zero_position_stocks)

    # Sort zero_position_stocks based on priority_list
    zero_position_stocks.sort(key=lambda x: priority_list.index(x) if x in priority_list else len(priority_list))

    allocation_plan = {}
    remaining_amount = new_amount

    # First, allocate to stocks we don't own
    for ticker in zero_position_stocks:
        price = comparison[ticker]['price']
        if remaining_amount >= price:
            allocation_plan[ticker] = price
            remaining_amount -= price
        else:
            break

    # If we have remaining amount, allocate to underweight positions
    if remaining_amount > 0:
        underweight_positions = sorted(
            [(ticker, data) for ticker, data in comparison.items() if data['difference'] > 0],
            key=lambda x: x[1]['difference'], reverse=True
        )

        for ticker, data in underweight_positions:
            price = data['price']
            difference = data['difference']

            if remaining_amount >= price:
                shares_to_buy = min(int(difference // price), int(remaining_amount // price))
                if shares_to_buy > 0:
                    amount_to_allocate = shares_to_buy * price
                    allocation_plan[ticker] = allocation_plan.get(ticker, 0) + amount_to_allocate
                    remaining_amount -= amount_to_allocate

            if remaining_amount < min(price for ticker, data in comparison.items()):
                break

    # Debug: Print allocation plan
    print("\nAllocation plan:")
    for ticker, amount in allocation_plan.items():
        print(f"{ticker}: ${amount:.2f}")

    return allocation_plan, remaining_amount
