# Personal ETF Creator

This project allows you to create a personalized ETF (Exchange-Traded Fund) by allocating stocks from different lists with custom weightings. It uses a geometric allocation strategy to distribute investments across selected stocks. The script now handles both your total portfolio and new investments separately.

## Features

- Define multiple stock lists for total portfolio and new investments
- Geometric allocation strategy for stock weighting
- Configurable maximum number of stocks and minimum dollar amount per stock
- Separate calculations for total portfolio and new investments
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

## Configuration

Update the `.env` file with your specific settings:

```
# Total portfolio stock list
STOCK_LIST_TOTAL=AVUV,IETC,BUG,XLV,SOXQ,AMZN,MELI,CCJ,TEVA,ZS,COST,PANW,ELF,MU,AMD,CEG,CHWY,GMED,VLTO,SNOW,IBM,AAPL

# New investment stock list
STOCK_LIST_NEW=AVUV,IETC,BUG,XLV,SOXQ

# Investment amounts
TOTAL_AMOUNT=7000
NEW_AMOUNT=1000

# Allocation parameters
GEOMETRIC_RATIO=0.8
STOCK_LIMIT=0
MIN_DOLLAR_AMOUNT=0
```

## Sample Output

Here's a sample output illustrating both the total portfolio and new investment allocations:

```
TOTAL Portfolio: $7000.00

Rank | Stock | Allocation | Dollar Amount
---------------------------------------
   1 | AVUV   |     20.08% | $    1405.31
   2 | IETC   |     16.06% | $    1124.25
   3 | BUG    |     12.85% | $     899.40
   4 | XLV    |     10.28% | $     719.52
   5 | SOXQ   |      8.22% | $     575.61
   6 | IVV    |      6.58% | $     460.49
   7 | AMZN   |      5.26% | $     368.39
   8 | MELI   |      4.21% | $     294.71
   9 | TEVA   |      3.37% | $     235.77
  10 | ZS     |      2.69% | $     188.62
  11 | COST   |      2.16% | $     150.89
  12 | PANW   |      1.72% | $     120.72
  13 | ELF    |      1.38% | $      96.57
  14 | CCJ    |      1.10% | $      77.26
  15 | ONON   |      0.88% | $      61.81
  16 | CHWY   |      0.71% | $      49.44
  17 | MU     |      0.57% | $      39.56
  18 | AMD    |      0.45% | $      31.64
  19 | CEG    |      0.36% | $      25.32
  20 | GMED   |      0.29% | $      20.25
  21 | VLTO   |      0.23% | $      16.20
  22 | SNOW   |      0.19% | $      12.96
  23 | IBM    |      0.15% | $      10.37
  24 | AAPL   |      0.12% | $       8.30
  25 | CMG    |      0.09% | $       6.64
---------------------------------------
Total:        |    100.00% | $    7000.00

NEW Portfolio: $1000.00

Rank | Stock | Allocation | Dollar Amount
---------------------------------------
   1 | AVUV   |     27.11% | $     271.06
   2 | IETC   |     21.68% | $     216.84
   3 | BUG    |     17.35% | $     173.48
   4 | XLV    |     13.88% | $     138.78
   5 | SOXQ   |     11.10% | $     111.02
   6 | IVV    |      8.88% | $      88.82
---------------------------------------
Total:        |    100.00% | $    1000.00
```

This output shows how the script allocates both your total portfolio and your new investment, allowing you to see where to put your new money every two weeks without fully reallocating the entire portfolio.

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
