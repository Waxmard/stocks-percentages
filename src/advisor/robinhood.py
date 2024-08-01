import os
import logging
from dotenv import load_dotenv
import robin_stocks.robinhood as r
from advisor.allocate import get_stock_allocations, get_stock_lists

load_dotenv(".env")

# Set up logging
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=log_level, format='%(message)s')
logger = logging.getLogger(__name__)

def login():
    r.login(os.getenv('ROBINHOOD_USERNAME'), os.getenv('ROBINHOOD_PASSWORD'))

def get_positions():
    login()
    return r.build_holdings()

def get_current_prices(tickers):
    return {ticker: float(r.stocks.get_latest_price(ticker)[0]) for ticker in tickers}

def compare_allocations_to_positions():
    allocations = get_stock_allocations()
    positions = get_positions()
    all_tickers = set(allocations.keys()) | set(positions.keys())
    current_prices = get_current_prices(all_tickers)

    return {
        ticker: {
            'difference': round(allocations.get(ticker, 0) - float(positions.get(ticker, {}).get('equity', 0)), 2),
            'price': current_prices[ticker],
            'current_equity': float(positions.get(ticker, {}).get('equity', 0)),
            'owned': ticker in positions
        } for ticker in all_tickers
    }

def get_priority_list(for_zero_positions=False):
    stock_lists = get_stock_lists()
    if for_zero_positions:
        categories = ['STRONG_BUY', 'BUY', 'MODERATE_BUY', 'ETF']
    else:
        categories = ['ETF', 'STRONG_BUY', 'BUY', 'MODERATE_BUY']
    return [stock for category in categories for stock in stock_lists.get(category, [''])[0]]

def get_stock_category(ticker):
    stock_lists = get_stock_lists()
    return next((category for category, (stocks, _, _) in stock_lists.items() if ticker in stocks), "UNKNOWN")

def allocate_funds(stocks, comparison, remaining_amount, allocation_type):
    allocation_plan = {}
    for ticker in stocks:
        price = comparison[ticker]['price']
        if remaining_amount >= price:
            if allocation_type == 'zero_position':
                amount_to_allocate = price
            else:  # underweight
                difference = comparison[ticker]['difference']
                shares_to_buy = min(int(difference // price), int(remaining_amount // price))
                amount_to_allocate = shares_to_buy * price

            if amount_to_allocate > 0:
                allocation_plan[ticker] = amount_to_allocate
                remaining_amount -= amount_to_allocate
                logger.info(f"Allocated ${amount_to_allocate:.2f} to {ticker} ({allocation_type})")
            else:
                logger.debug(f"No additional shares needed for {ticker}")
        else:
            logger.debug(f"Not enough funds to allocate to {ticker}")
            break

    return allocation_plan, remaining_amount

def balance_priority_lists(allocation_plan, comparison, remaining_amount):
    category_order = ['ETF', 'STRONG_BUY', 'BUY', 'MODERATE_BUY']
    category_max_values = {category: max((allocation_plan.get(ticker, 0) for ticker in comparison if get_stock_category(ticker) == category), default=0) for category in category_order}

    logger.info("\nBalancing priority lists:")
    logger.debug(f"Initial allocation plan: {allocation_plan}")
    logger.info(f"Remaining amount: ${remaining_amount:.2f}")
    logger.debug(f"Maximum values per category: {category_max_values}")

    for i in range(len(category_order) - 1):
        higher_category, lower_category = category_order[i], category_order[i+1]
        logger.debug(f"\nComparing {higher_category} with {lower_category}")
        logger.debug(f"{higher_category} max: ${category_max_values[higher_category]:.2f}")
        logger.debug(f"{lower_category} max: ${category_max_values[lower_category]:.2f}")

        if category_max_values[higher_category] <= category_max_values[lower_category]:
            difference = category_max_values[lower_category] - category_max_values[higher_category]
            logger.info(f"Need to add ${difference:.2f} to {higher_category} stocks")

            for ticker in allocation_plan:
                if get_stock_category(ticker) == higher_category:
                    amount_to_add = min(difference, remaining_amount)
                    allocation_plan[ticker] += amount_to_add
                    remaining_amount -= amount_to_add
                    category_max_values[higher_category] += amount_to_add
                    logger.info(f"Added ${amount_to_add:.2f} to {ticker}")
                    logger.debug(f"New allocation for {ticker}: ${allocation_plan[ticker]:.2f}")
                    logger.debug(f"Remaining amount: ${remaining_amount:.2f}")
                    break

            if remaining_amount == 0:
                break

    logger.info(f"\nFinal allocation plan after balancing: {allocation_plan}")
    logger.info(f"Remaining amount after balancing: ${remaining_amount:.2f}")
    return allocation_plan, remaining_amount

def allocate_new_investment():
    new_amount = float(os.getenv('NEW_AMOUNT', 0))
    comparison = compare_allocations_to_positions()

    logger.info(f"\nStarting new investment allocation with ${new_amount:.2f}")
    logger.debug(f"All stocks in comparison: {comparison}")

    zero_position_priority_list = get_priority_list(for_zero_positions=True)
    logger.debug(f"Zero position priority list: {zero_position_priority_list}")

    zero_position_stocks = [ticker for ticker, data in comparison.items() if not data['owned']]
    sorted_zero_position_stocks = sorted(zero_position_stocks, key=lambda x: zero_position_priority_list.index(x) if x in zero_position_priority_list else len(zero_position_priority_list))
    logger.debug(f"Sorted zero position stocks: {sorted_zero_position_stocks}")

    logger.info("\nAllocating to zero positions:")
    allocation_plan, remaining_amount = allocate_funds(sorted_zero_position_stocks, comparison, new_amount, 'zero_position')

    logger.info(f"\nRemaining amount after zero position allocation: ${remaining_amount:.2f}")

    allocation_plan, remaining_amount = balance_priority_lists(allocation_plan, comparison, remaining_amount)

    if remaining_amount > 0:
        logger.debug("\nAllocating to underweight positions:")
        underweight_priority_list = get_priority_list(for_zero_positions=False)
        underweight_positions = sorted(
            [(ticker, data) for ticker, data in comparison.items() if data['difference'] > 0],
            key=lambda x: (underweight_priority_list.index(x[0]) if x[0] in underweight_priority_list else len(underweight_priority_list), -x[1]['difference'])
        )
        logger.debug(f"Underweight positions: {underweight_positions}")
        underweight_allocation, remaining_amount = allocate_funds([ticker for ticker, _ in underweight_positions], comparison, remaining_amount, 'underweight')
        allocation_plan.update(underweight_allocation)

    logger.info("\nFinal allocation plan:")
    for ticker, amount in allocation_plan.items():
        logger.info(f"{ticker}: ${amount:.2f}")

    logger.info(f"\nRemaining unallocated amount: ${remaining_amount:.2f}")

    return allocation_plan, remaining_amount
