# Personal ETF Creator

This project allows you to create a personalized ETF (Exchange-Traded Fund) by allocating stocks from different tiers with custom weightings. It uses a geometric allocation strategy to distribute investments across selected stocks within each tier.

## Features

- Define multiple stock tiers (ETF, Strong Buy, Buy, Moderate Buy)
- Customize allocation percentages for each tier
- Geometric allocation strategy for stock weighting within ordered tiers
- Equal allocation for unordered tiers
- Configurable geometric ratio for ordered allocations

## Important Note: Stock Order Matters in Ordered Tiers!

For tiers marked as ordered (e.g., ETF_ORDERED=true), the order of stocks is critically important for the allocation process. The geometric allocation strategy assigns higher weights to stocks listed earlier in the list. This means:

1. Stocks listed first will receive larger allocations.
2. Changing the order of stocks can significantly alter the final allocation.

Always carefully consider the order when defining your stock lists for ordered tiers in the `.env` file.

## Prerequisites

- Python 3.12
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

Run the tiered script to generate your personal ETF allocation:
```sh
make run
```

## Configuration

Update the `.env` file with your specific settings. Here's an example configuration:

```
# ETF stocks (ordered)
ETF=AVUV,IETC,BUG,XLV,SOXQ,IVV
ETF_ALLOCATION=50
ETF_ORDERED=true

# Strong buy stocks (unordered)
STRONG_BUY=AMZN,MELI,TEVA,ZS,COST,PANW,ELF,CCJ,HAL
STRONG_BUY_ALLOCATION=25
STRONG_BUY_ORDERED=false

# Buy stocks (unordered)
BUY=ONON,CHWY,MU,AMD,CEG
BUY_ALLOCATION=15
BUY_ORDERED=false

# Moderate buy stocks (unordered)
MODERATE_BUY=GMED,VLTO,SNOW,IBM,AAPL,CMG,HON
MODERATE_BUY_ALLOCATION=10
MODERATE_BUY_ORDERED=false

# Investment amount
TOTAL_AMOUNT=7000

# Allocation parameters
GEOMETRIC_RATIO=0.8
```

## Sample Output

Here's a sample output illustrating the tiered allocation:

```
TOTAL Portfolio: $7000.00

Rank | Stock | Allocation | Dollar Amount
---------------------------------------
   1 | AVUV   |     13.55% | $     948.69
   2 | IETC   |     10.84% | $     758.96
   3 | BUG    |      8.67% | $     607.16
   4 | XLV    |      6.94% | $     485.73
   5 | SOXQ   |      5.55% | $     388.59
   6 | IVV    |      4.44% | $     310.87
   7 | ONON   |      3.00% | $     210.00
   8 | CHWY   |      3.00% | $     210.00
   9 | MU     |      3.00% | $     210.00
  10 | AMD    |      3.00% | $     210.00
  11 | CEG    |      3.00% | $     210.00
  12 | AMZN   |      2.78% | $     194.44
  13 | MELI   |      2.78% | $     194.44
  14 | TEVA   |      2.78% | $     194.44
  15 | ZS     |      2.78% | $     194.44
  16 | COST   |      2.78% | $     194.44
  17 | PANW   |      2.78% | $     194.44
  18 | ELF    |      2.78% | $     194.44
  19 | CCJ    |      2.78% | $     194.44
  20 | HAL    |      2.78% | $     194.44
  21 | GMED   |      1.43% | $     100.00
  22 | VLTO   |      1.43% | $     100.00
  23 | SNOW   |      1.43% | $     100.00
  24 | IBM    |      1.43% | $     100.00
  25 | AAPL   |      1.43% | $     100.00
  26 | CMG    |      1.43% | $     100.00
  27 | HON    |      1.43% | $     100.00
---------------------------------------
Total:        |    100.00% | $    7000.00
```

This output shows how the script allocates your portfolio across different tiers, with geometric allocation for ordered tiers and equal allocation for unordered tiers.

## Development

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

- `tiered.py`: The main script that generates the tiered ETF allocation
- `combined.py`: An alternative script for combined allocation (if needed)
- `requirements.in`: Direct project dependencies
- `requirements.txt`: Pinned dependencies (generated from requirements.in)
- `Makefile`: Defines common development tasks
- `.env`: Configuration file for stock tiers and allocations (not in version control)
- `.env.example`: Example configuration file

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
