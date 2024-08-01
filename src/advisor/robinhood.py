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

def get_priority_list():
    stock_lists = get_stock_lists()
    priority_list = []
    for category in ['ETF', 'STRONG_BUY', 'BUY', 'MODERATE_BUY']:
        if category in stock_lists:
            priority_list.extend(stock_lists[category][0])
    return priority_list

def get_category_order():
    return ['ETF', 'STRONG_BUY', 'BUY', 'MODERATE_BUY']

def get_zero_position_stocks(comparison):
    return [ticker for ticker, data in comparison.items() if not data['owned']]

def sort_zero_position_stocks(zero_position_stocks, priority_list):
    return sorted(zero_position_stocks,
                  key=lambda x: priority_list.index(x) if x in priority_list else len(priority_list))

def allocate_to_zero_positions(zero_position_stocks, comparison, remaining_amount):
    allocation_plan = {}
    for ticker in zero_position_stocks:
        price = comparison[ticker]['price']
        if remaining_amount >= price:
            allocation_plan[ticker] = price
            remaining_amount -= price
            print(f"Allocated ${price:.2f} to {ticker} (zero position)")
        else:
            print(f"Not enough funds to allocate to {ticker}")
            break
    return allocation_plan, remaining_amount

def get_underweight_positions(comparison):
    return sorted(
        [(ticker, data) for ticker, data in comparison.items() if data['difference'] > 0],
        key=lambda x: x[1]['difference'], reverse=True
    )

def allocate_to_underweight_positions(underweight_positions, comparison, remaining_amount):
    allocation_plan = {}
    for ticker, data in underweight_positions:
        price = data['price']
        difference = data['difference']

        if remaining_amount >= price:
            shares_to_buy = min(int(difference // price), int(remaining_amount // price))
            if shares_to_buy > 0:
                amount_to_allocate = shares_to_buy * price
                allocation_plan[ticker] = amount_to_allocate
                remaining_amount -= amount_to_allocate
                print(f"Allocated ${amount_to_allocate:.2f} to {ticker} (underweight)")
            else:
                print(f"No additional shares needed for {ticker}")
        else:
            print(f"Not enough funds to allocate to {ticker}")

        if remaining_amount < min(price for ticker, data in comparison.items()):
            print("Remaining amount is less than the cheapest stock price. Stopping allocation.")
            break

    return allocation_plan, remaining_amount

def get_stock_category(ticker):
    stock_lists = get_stock_lists()
    for category, (stocks, _, _) in stock_lists.items():
        if ticker in stocks:
            return category
    return "UNKNOWN"

def balance_priority_lists(allocation_plan, comparison, remaining_amount):
    category_order = get_category_order()
    category_max_values = {category: 0 for category in category_order}

    print("\nBalancing priority lists:")
    print("Initial allocation plan:", allocation_plan)
    print(f"Remaining amount: ${remaining_amount:.2f}")

    # Calculate the maximum allocation for each category
    for ticker, amount in allocation_plan.items():
        category = get_stock_category(ticker)
        category_max_values[category] = max(category_max_values[category], amount)

    print("Maximum values per category:", category_max_values)

    # Balance allocations across priority lists
    for i in range(len(category_order) - 1):
        higher_category = category_order[i]
        lower_category = category_order[i + 1]

        print(f"\nComparing {higher_category} with {lower_category}")
        print(f"{higher_category} max: ${category_max_values[higher_category]:.2f}")
        print(f"{lower_category} max: ${category_max_values[lower_category]:.2f}")

        if category_max_values[higher_category] <= category_max_values[lower_category]:
            difference = category_max_values[lower_category] - category_max_values[higher_category]
            print(f"Need to add ${difference:.2f} to {higher_category} stocks")

            for ticker in allocation_plan:
                if get_stock_category(ticker) == higher_category:
                    if remaining_amount >= difference:
                        allocation_plan[ticker] += difference
                        remaining_amount -= difference
                        category_max_values[higher_category] += difference
                        print(f"Added ${difference:.2f} to {ticker}")
                        print(f"New allocation for {ticker}: ${allocation_plan[ticker]:.2f}")
                        print(f"Remaining amount: ${remaining_amount:.2f}")
                        break
                    else:
                        print(f"Not enough funds to fully balance. Adding remaining ${remaining_amount:.2f} to {ticker}")
                        allocation_plan[ticker] += remaining_amount
                        remaining_amount = 0
                        break

    print("\nFinal allocation plan after balancing:", allocation_plan)
    print(f"Remaining amount after balancing: ${remaining_amount:.2f}")
    return allocation_plan, remaining_amount

def allocate_new_investment():
    new_amount = float(os.getenv('NEW_AMOUNT', 0))
    comparison = compare_allocations_to_positions()

    print(f"\nStarting new investment allocation with ${new_amount:.2f}")
    print("\nAll stocks in comparison:")
    for ticker, data in comparison.items():
        print(f"{ticker}: {data}")

    priority_list = get_priority_list()
    print("\nPriority list:", priority_list)

    zero_position_stocks = get_zero_position_stocks(comparison)
    print("\nZero position stocks:", zero_position_stocks)

    sorted_zero_position_stocks = sort_zero_position_stocks(zero_position_stocks, priority_list)
    print("\nSorted zero position stocks:", sorted_zero_position_stocks)

    print("\nAllocating to zero positions:")
    allocation_plan, remaining_amount = allocate_to_zero_positions(sorted_zero_position_stocks, comparison, new_amount)

    print(f"\nRemaining amount after zero position allocation: ${remaining_amount:.2f}")

    allocation_plan, remaining_amount = balance_priority_lists(allocation_plan, comparison, remaining_amount)

    if remaining_amount > 0:
        print("\nAllocating to underweight positions:")
        underweight_positions = get_underweight_positions(comparison)
        print("Underweight positions:", underweight_positions)
        underweight_allocation, remaining_amount = allocate_to_underweight_positions(underweight_positions, comparison, remaining_amount)
        allocation_plan.update(underweight_allocation)

    print("\nFinal allocation plan:")
    for ticker, amount in allocation_plan.items():
        print(f"{ticker}: ${amount:.2f}")

    print(f"\nRemaining unallocated amount: ${remaining_amount:.2f}")

    return allocation_plan, remaining_amount
