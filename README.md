# Personal ETF Creator

This project allows you to create a personalized ETF (Exchange-Traded Fund) by allocating stocks from different lists with custom weightings. It uses a geometric allocation strategy to distribute investments across selected stocks.

## Features

- Define multiple stock lists with custom allocations
- Geometric allocation strategy for stock weighting
- Configurable maximum number of stocks and minimum dollar amount per stock
- Automated requirements management and virtual environment setup

## Important Note: Stock Order Matters!

The order of stocks in your lists is critically important for the allocation process. The geometric allocation strategy assigns higher weights to stocks listed earlier in each list. This means:

1. Stocks listed first will receive larger allocations.
2. Changing the order of stocks can significantly alter the final allocation.

Always carefully consider the order when defining your stock lists in the `.env` file.

## Prerequisites

- Python 3.7+
- make (usually pre-installed on macOS and Linux)

## Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/personal-etf-creator.git
   cd personal-etf-creator
   ```

2. Set up the project:
   ```sh
   make setup
   ```
   This command creates a virtual environment and installs all necessary dependencies.

3. Create a `.env` file in the project root and configure your preferences. Use `.env.example` as a starting point:
   ```sh
   cp .env.example .env
   ```
   Edit the `.env` file to match your desired stock lists and allocations.

## Usage

Run the main script to generate your personal ETF allocation:
```sh
make run
```

## Sample Outputs

Here are some sample outputs to illustrate how the allocation works and the importance of stock order:

### Example 1: Default Configuration

```
Total Portfolio: $20000.00

Rank | Stock | Allocation | Dollar Amount
---------------------------------------
   1 | CRWD   |     15.72% | $    3143.33
   2 | KNSL   |     13.36% | $    2671.83
   3 | CAVA   |     11.36% | $    2271.06
   4 | TTD    |      9.65% | $    1930.40
   5 | TMDX   |      8.20% | $    1640.84
   6 | AMZN   |      6.97% | $    1394.71
   7 | ARM    |      5.93% | $    1185.51
   8 | ABNB   |      5.04% | $    1007.68
   9 | SNOW   |      4.28% | $     856.53
  10 | SHOP   |      3.64% | $     728.05
  11 | MELI   |      3.09% | $     618.84
  12 | META   |      2.63% | $     526.02
  13 | CHWY   |      2.24% | $     447.11
  14 | TSLA   |      1.90% | $     380.05
  15 | IBM    |      1.62% | $     323.04
  16 | SMCI   |      1.37% | $     274.58
  17 | NVIDIA |      1.17% | $     233.40
  18 | MU     |      0.99% | $     198.39
  19 | AMD    |      0.84% | $     168.63
---------------------------------------
Total:        |    100.00% | $   20000.00
```

### Example 2: Changing Stock Order

If we move TSLA to the top of the list:

```
Total Portfolio: $20000.00

Rank | Stock | Allocation | Dollar Amount
---------------------------------------
   1 | CRWD   |     15.72% | $    3143.33
   2 | TSLA   |     13.36% | $    2671.83
   3 | CAVA   |     11.36% | $    2271.06
   4 | KNSL   |      9.65% | $    1930.40
   5 | TMDX   |      8.20% | $    1640.84
   6 | AMZN   |      6.97% | $    1394.71
   7 | ARM    |      5.93% | $    1185.51
   8 | TTD    |      5.04% | $    1007.68
   9 | ABNB   |      4.28% | $     856.53
  10 | SNOW   |      3.64% | $     728.05
  11 | SHOP   |      3.09% | $     618.84
  12 | MELI   |      2.63% | $     526.02
  13 | META   |      2.24% | $     447.11
  14 | CHWY   |      1.90% | $     380.05
  15 | IBM    |      1.62% | $     323.04
  16 | SMCI   |      1.37% | $     274.58
  17 | NVIDIA |      1.17% | $     233.40
  18 | MU     |      0.99% | $     198.39
  19 | AMD    |      0.84% | $     168.63
---------------------------------------
Total:        |    100.00% | $   20000.00
```

Notice how TSLA now has the second highest allocation, significantly changing the distribution of funds.

### Example 3: With Stock Limit and Minimum Dollar Amount

Setting STOCK_LIMIT=5 and MIN_DOLLAR_AMOUNT=1000:

```
Total Portfolio: $20000.00

Rank | Stock | Allocation | Dollar Amount
---------------------------------------
   1 | CRWD   |     26.96% | $    5392.83
   2 | KNSL   |     22.92% | $    4583.90
   3 | CAVA   |     19.48% | $    3896.32
   4 | TTD    |     16.56% | $    3311.87
   5 | TMDX   |     14.08% | $    2815.09
---------------------------------------
Total:        |    100.00% | $   20000.00
```

This example shows how the stock limit and minimum dollar amount affect the allocation, concentrating the investment in fewer stocks while ensuring each has a significant allocation.

## Development

### Running Tests

To run the unit tests:
```sh
make test
```

### Updating Requirements

To update the project dependencies:
```sh
make update-requirements
```

### Linting

To run linters and code formatters:
```sh
make lint
```

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. To install the hooks:
```sh
make setup
pre-commit install
```

## Project Structure

- `main.py`: The main script that generates the ETF allocation
- `test_main.py`: Unit tests for the main script
- `requirements.in`: Direct project dependencies
- `requirements.txt`: Pinned dependencies (generated from requirements.in)
- `Makefile`: Defines common development tasks
- `.env`: Configuration file for stock lists and allocations (not in version control)
- `.env.example`: Example configuration file

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
