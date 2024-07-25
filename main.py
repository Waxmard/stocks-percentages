import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_stock_lists():
    stock_lists = {}
    for key, value in os.environ.items():
        if key.startswith("STOCK_LIST_"):
            list_id = key.split("_")[-1]
            stock_lists[list_id] = value.split(",")
    return stock_lists


def allocate_stocks(stocks, ratio):
    weights = [ratio**i for i in range(len(stocks))]
    total_weight = sum(weights)
    percentages = [weight / total_weight * 100 for weight in weights]
    return dict(zip(stocks, percentages))


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


def print_allocations(allocations, total_amount, title):
    print(f"\n{title}: ${total_amount:.2f}")
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


def main():
    total_amount = float(os.getenv("TOTAL_AMOUNT"))
    new_amount = float(os.getenv("NEW_AMOUNT"))
    geometric_ratio = float(os.getenv("GEOMETRIC_RATIO"))
    stock_limit = int(os.getenv("STOCK_LIMIT", "0"))
    min_dollar_amount = float(os.getenv("MIN_DOLLAR_AMOUNT", "0"))

    stock_lists = get_stock_lists()

    for list_id, amount in [("TOTAL", total_amount), ("NEW", new_amount)]:
        stocks = stock_lists[list_id]
        allocations = allocate_stocks(stocks, geometric_ratio)
        final_allocations = limit_and_reallocate(
            allocations,
            stock_limit,
            geometric_ratio,
            amount,
            min_dollar_amount,
        )
        print_allocations(final_allocations, amount, f"{list_id} Portfolio")


if __name__ == "__main__":
    main()
