import os
from dotenv import load_dotenv
from collections import defaultdict

# Load environment variables
load_dotenv()

# Constants for stock lists
MOTLEY = os.getenv("MOTLEY_STOCKS").split(",")
TED = os.getenv("TED_STOCKS").split(",")
ME = os.getenv("ME_STOCKS").split(",")

# Constants for portfolio allocation
MOTLEY_ALLOCATION = float(os.getenv("MOTLEY_ALLOCATION"))
TED_ALLOCATION = float(os.getenv("TED_ALLOCATION"))
ME_ALLOCATION = float(os.getenv("ME_ALLOCATION"))

# Constants for stock limit and minimum dollar amount
STOCK_LIMIT = int(os.getenv("STOCK_LIMIT", "0"))  # Default to 0 (no limit) if not set
MIN_DOLLAR_AMOUNT = float(
    os.getenv("MIN_DOLLAR_AMOUNT", "0")
)  # Default to 0 (no minimum) if not set


def allocate_stocks(stocks, total_percentage, ratio):
    """
    Allocate percentages to stocks using a geometric sequence.

    :param stocks: List of stock names
    :param total_percentage: Total percentage to allocate for this list
    :param ratio: Ratio for the geometric sequence (default 0.8)
    :return: Dictionary of stock names with their allocated percentages
    """
    weights = [ratio**i for i in range(len(stocks))]
    total_weight = sum(weights)
    percentages = [weight / total_weight * total_percentage for weight in weights]
    return dict(zip(stocks, percentages))


def combine_allocations(allocations_list):
    """
    Combine multiple allocation dictionaries into a single dictionary.

    :param allocations_list: List of allocation dictionaries
    :return: Combined dictionary of stock names with their total allocated percentages
    """
    combined = defaultdict(float)
    for allocations in allocations_list:
        for stock, percentage in allocations.items():
            combined[stock] += percentage
    return dict(combined)


def print_allocations(allocations, total_amount):
    """
    Print the allocations for each stock, including rank, percentages and dollar amounts.

    :param allocations: Dictionary of stock names with their allocated percentages
    :param total_amount: Total portfolio amount in dollars
    """
    print(f"Total Portfolio: ${total_amount:.2f}")
    print("\nRank | Stock | Allocation | Dollar Amount")
    print("---------------------------------------")
    total_percentage = 0
    total_dollars = 0
    for rank, (stock, percentage) in enumerate(
        sorted(allocations.items(), key=lambda x: x[1], reverse=True), 1
    ):
        dollars = percentage / 100 * total_amount
        print(f"{rank:4d} | {stock:<6} | {percentage:>9.2f}% | ${dollars:>11.2f}")
        total_percentage += percentage
        total_dollars += dollars
    print("---------------------------------------")
    print(f"Total:        | {total_percentage:>9.2f}% | ${total_dollars:>11.2f}")


def limit_and_reallocate(allocations, limit, ratio, total_amount, min_dollar_amount):
    """
    Limit the number of stocks, reallocate percentages to total 100%, and ensure minimum dollar amount.

    :param allocations: Dictionary of stock allocations
    :param limit: Maximum number of stocks to keep
    :param ratio: Ratio for geometric reallocation
    :param total_amount: Total portfolio amount in dollars
    :param min_dollar_amount: Minimum dollar amount for each stock
    :return: New dictionary of limited and reallocated stocks
    """
    if limit <= 0 or limit >= len(allocations):
        limit = len(allocations)

    # Sort stocks by allocation percentage
    sorted_stocks = sorted(allocations.items(), key=lambda x: x[1], reverse=True)

    while len(sorted_stocks) > 1:  # Ensure we always keep at least one stock
        # Keep only the top 'limit' stocks
        top_stocks = sorted_stocks[:limit]

        # Reallocate to the top stocks using the same geometric ratio, ensuring total is 100%
        stock_names = [stock for stock, _ in top_stocks]
        weights = [ratio**i for i in range(len(stock_names))]
        total_weight = sum(weights)
        percentages = [weight / total_weight * 100 for weight in weights]

        new_allocations = dict(zip(stock_names, percentages))

        # Check if all stocks meet the minimum dollar amount
        if all(
            (percentage / 100 * total_amount) >= min_dollar_amount
            for percentage in new_allocations.values()
        ):
            return new_allocations

        # If not all stocks meet the minimum, reduce the limit and try again
        limit -= 1
        sorted_stocks = sorted_stocks[:limit]

    # If we can't meet the minimum dollar amount for multiple stocks, just return the top stock with 100% allocation
    return {sorted_stocks[0][0]: 100.0}


def main():
    """
    Main function to run the stock allocation program.
    """
    total_amount = float(os.getenv("TOTAL_AMOUNT"))
    geometric_ratio = float(os.getenv("GEOMETRIC_RATIO"))

    # Allocate stocks for each list
    motley_allocations = allocate_stocks(MOTLEY, MOTLEY_ALLOCATION, geometric_ratio)
    ted_allocations = allocate_stocks(TED, TED_ALLOCATION, geometric_ratio)
    me_allocations = allocate_stocks(ME, ME_ALLOCATION, geometric_ratio)

    # Combine allocations
    combined_allocations = combine_allocations(
        [motley_allocations, ted_allocations, me_allocations]
    )

    # Apply stock limit, reallocate, and ensure minimum dollar amount
    final_allocations = limit_and_reallocate(
        combined_allocations,
        STOCK_LIMIT,
        geometric_ratio,
        total_amount,
        MIN_DOLLAR_AMOUNT,
    )

    # Print final allocations
    print_allocations(final_allocations, total_amount)


if __name__ == "__main__":
    main()
