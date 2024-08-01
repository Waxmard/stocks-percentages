import os
from dotenv import load_dotenv
import robin_stocks.robinhood as r
from advisor.allocate import get_stock_allocations

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

    # Get all unique tickers from both allocations and positions
    all_tickers = set(allocations.keys()) | set(positions.keys())

    # Get current prices for all tickers
    current_prices = get_current_prices(all_tickers)

    comparison = {}

    for ticker in all_tickers:
        allocated_amount = allocations.get(ticker, 0)
        current_equity = float(positions[ticker]['equity']) if ticker in positions else 0
        difference = allocated_amount - current_equity
        price = current_prices[ticker]

        comparison[ticker] = {
            'difference': round(difference, 2),
            'price': price
        }

    return comparison
