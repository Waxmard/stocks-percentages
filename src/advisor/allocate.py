import os
from dotenv import load_dotenv

load_dotenv(".env")


def get_stock_lists():
    return {
        "ETF": (
            os.getenv("ETF", "").split(","),
            float(os.getenv("ETF_ALLOCATION", 0)) / 100,
            os.getenv("ETF_ORDERED", "true").lower() == "true",
        ),
        "STRONG_BUY": (
            os.getenv("STRONG_BUY", "").split(","),
            float(os.getenv("STRONG_BUY_ALLOCATION", 0)) / 100,
            os.getenv("STRONG_BUY_ORDERED", "false").lower() == "true",
        ),
        "BUY": (
            os.getenv("BUY", "").split(","),
            float(os.getenv("BUY_ALLOCATION", 0)) / 100,
            os.getenv("BUY_ORDERED", "false").lower() == "true",
        ),
        "MODERATE_BUY": (
            os.getenv("MODERATE_BUY", "").split(","),
            float(os.getenv("MODERATE_BUY_ALLOCATION", 0)) / 100,
            os.getenv("MODERATE_BUY_ORDERED", "false").lower() == "true",
        ),
    }


def allocate_stocks(stocks, ratio):
    weights = [ratio**i for i in range(len(stocks))]
    total_weight = sum(weights)
    percentages = [weight / total_weight * 100 for weight in weights]
    return dict(zip(stocks, percentages))


def get_stock_allocations():
    total_amount = float(os.getenv("TOTAL_AMOUNT"))
    geometric_ratio = float(os.getenv("GEOMETRIC_RATIO"))
    stock_lists = get_stock_lists()

    total_allocations = {}
    for category, (stocks, category_allocation, ordered) in stock_lists.items():
        category_amount = total_amount * category_allocation

        if ordered:
            allocations = allocate_stocks(stocks, geometric_ratio)
        else:
            equal_percentage = 100 / len(stocks)
            allocations = {stock: equal_percentage for stock in stocks}

        for stock, percentage in allocations.items():
            stock_allocation = (percentage / 100) * category_amount
            if stock in total_allocations:
                total_allocations[stock] += stock_allocation
            else:
                total_allocations[stock] = stock_allocation

    return total_allocations

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


def run():
    total_amount = float(os.getenv("TOTAL_AMOUNT"))
    geometric_ratio = float(os.getenv("GEOMETRIC_RATIO"))
    stock_lists = get_stock_lists()

    total_allocations = {}
    for category, (stocks, category_allocation, ordered) in stock_lists.items():
        category_amount = total_amount * category_allocation

        if ordered:
            allocations = allocate_stocks(stocks, geometric_ratio)
        else:
            equal_percentage = 100 / len(stocks)
            allocations = {stock: equal_percentage for stock in stocks}

        for stock, percentage in allocations.items():
            stock_allocation = (percentage / 100) * category_amount
            if stock in total_allocations:
                total_allocations[stock] += stock_allocation
            else:
                total_allocations[stock] = stock_allocation

    # Convert dollar amounts back to percentages
    total_allocations = {
        stock: (amount / total_amount) * 100
        for stock, amount in total_allocations.items()
    }

    print_allocations(total_allocations, total_amount, "TOTAL Portfolio")
