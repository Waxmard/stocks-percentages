import os
from dotenv import load_dotenv
from collections import defaultdict

# Load environment variables
load_dotenv()


def get_stock_lists():
    stock_lists = {}
    for key, value in os.environ.items():
        if key.startswith("STOCK_LIST_"):
            list_id = key.split("_")[-1]
            stock_lists[list_id] = value.split(",")
    return stock_lists


def get_allocations():
    allocations = {}
    for key, value in os.environ.items():
        if key.startswith("ALLOCATION_"):
            list_id = key.split("_")[-1]
            allocations[list_id] = float(value)
    return allocations


def allocate_stocks(stocks, total_percentage, ratio):
    weights = [ratio**i for i in range(len(stocks))]
    total_weight = sum(weights)
    percentages = [weight / total_weight * total_percentage for weight in weights]
    return dict(zip(stocks, percentages))


def combine_allocations(allocations_list):
    combined = defaultdict(float)
    for allocations in allocations_list:
        for stock, percentage in allocations.items():
            combined[stock] += percentage
    return dict(combined)


def print_allocations(allocations, total_amount):
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
    if limit <= 0 or limit >= len(allocations):
        limit = len(allocations)

    sorted_stocks = sorted(allocations.items(), key=lambda x: x[1], reverse=True)

    while len(sorted_stocks) > 1:
        top_stocks = sorted_stocks[:limit]

        stock_names = [stock for stock, _ in top_stocks]
        weights = [ratio**i for i in range(len(stock_names))]
        total_weight = sum(weights)
        percentages = [weight / total_weight * 100 for weight in weights]

        new_allocations = dict(zip(stock_names, percentages))

        if all(
            (percentage / 100 * total_amount) >= min_dollar_amount
            for percentage in new_allocations.values()
        ):
            return new_allocations

        limit -= 1
        sorted_stocks = sorted_stocks[:limit]

    return {sorted_stocks[0][0]: 100.0}


def validate_inputs(stock_lists, allocations):
    stock_list_ids = set(stock_lists.keys())
    allocation_ids = set(allocations.keys())

    if stock_list_ids != allocation_ids:
        missing_stocks = allocation_ids - stock_list_ids
        missing_allocations = stock_list_ids - allocation_ids
        error_message = (
            "Mismatch between STOCK_LIST and ALLOCATION environment variables\n"
        )
        if missing_stocks:
            error_message += (
                f"Missing stock lists for allocations: {', '.join(missing_stocks)}\n"
            )
        if missing_allocations:
            error_message += f"Missing allocations for stock lists: {', '.join(missing_allocations)}\n"
        raise ValueError(error_message)

    total_allocation = sum(allocations.values())
    if abs(total_allocation - 100) > 0.01:
        raise ValueError(
            f"Sum of allocation percentages must equal 100, but it's {total_allocation}"
        )


def main():
    total_amount = float(os.getenv("TOTAL_AMOUNT"))
    geometric_ratio = float(os.getenv("GEOMETRIC_RATIO"))
    stock_limit = int(os.getenv("STOCK_LIMIT", "0"))
    min_dollar_amount = float(os.getenv("MIN_DOLLAR_AMOUNT", "0"))

    stock_lists = get_stock_lists()
    allocations = get_allocations()

    validate_inputs(stock_lists, allocations)

    individual_allocations = []
    for list_id, stocks in stock_lists.items():
        individual_allocations.append(
            allocate_stocks(stocks, allocations[list_id], geometric_ratio)
        )

    combined_allocations = combine_allocations(individual_allocations)

    final_allocations = limit_and_reallocate(
        combined_allocations,
        stock_limit,
        geometric_ratio,
        total_amount,
        min_dollar_amount,
    )

    print_allocations(final_allocations, total_amount)


if __name__ == "__main__":
    main()
