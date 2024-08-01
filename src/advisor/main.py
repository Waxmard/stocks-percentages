from advisor.allocate import run, get_stock_allocations
from advisor.robinhood import get_positions

if __name__ == "__main__":
    # run()
    print('get_stock_allocations')
    print(get_stock_allocations())
    print()
    print('robinhood.py get_positions')
    print(get_positions())
