import os
from dotenv import load_dotenv
import robin_stocks.robinhood as r
from advisor.allocate import get_stock_allocations

load_dotenv(".env")


def get_positions():
    r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))
    return r.build_holdings()

def pretty_print_positions():
    for ticker, data in get_positions().items():
        print(f"Stock: {ticker}")
        print(f"Quantity: {data['quantity']}")
        print(f"Average Buy Price: ${data['average_buy_price']}")
        print(f"Current Price: ${data['price']}")
        print(f"Total Equity: ${data['equity']}")
        print("---")
