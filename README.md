# Robinhood Portfolio Optimizer and Investment Advisor

This project is a sophisticated investment tool that integrates with your Robinhood account to optimize your portfolio and provide intelligent investment advice. It analyzes your current holdings, compares them to a customizable target allocation, and offers recommendations for both rebalancing your existing portfolio and allocating new investments.

## Overview

The Robinhood Portfolio Optimizer and Investment Advisor offers a comprehensive solution for managing your Robinhood investments:

1. **Portfolio Analysis**: Fetches and analyzes your current Robinhood holdings in real-time.
2. **Custom Allocation Strategy**: Allows you to define a personalized target allocation across multiple tiers of stocks (e.g., ETFs, Strong Buy, Buy, Moderate Buy).
3. **Rebalancing Recommendations**: Compares your actual portfolio to your target allocation and suggests trades to bring them into alignment.
4. **New Investment Advice**: Provides specific recommendations on how to invest new funds, taking into account your current holdings and target allocation.
5. **Robinhood Integration**: Leverages the Robinhood API to fetch real-time data and potentially execute trades (if implemented).

This tool is designed for investors who want to maintain a specific portfolio allocation while taking advantage of Robinhood's platform. It's particularly useful for those who follow a tiered investment strategy, with different levels of conviction or types of investments.

## Key Features

- **Robinhood API Integration**: Seamlessly connects with your Robinhood account to fetch current holdings and real-time stock prices.
- **Customizable Allocation Strategy**:
  - Define multiple stock tiers (e.g., ETF, Strong Buy, Buy, Moderate Buy) with custom allocations.
  - Use a geometric allocation strategy for ordered tiers (e.g., for ETFs where order matters).
  - Apply equal allocation for unordered tiers.
- **Smart Investment Advice**:
  - Provides recommendations for rebalancing your current portfolio.
  - Offers guidance on allocating new investments based on your current holdings and target allocations.
- **Real-time Portfolio Analysis**: Compares your actual Robinhood portfolio to your target allocations, highlighting discrepancies.
- **Flexible Configuration**: Easily adjustable settings through a `.env` file, including Robinhood credentials and allocation preferences.

## Prerequisites

- Python 3.12
- make (usually pre-installed on macOS and Linux)
- Robinhood account credentials

## Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/personal-etf-creator.git
   cd personal-etf-creator
   ```

2. Set up the project:
   ```sh
   make install
   ```
   This command creates a virtual environment and installs all necessary dependencies, including the Robinhood API client.

3. Create a `.env` file in the project root and configure your preferences and Robinhood credentials:
   ```sh
   cp .env.example .env
   ```
   Edit the `.env` file to include your Robinhood username and password, along with your desired stock lists and allocations.

## Usage

Activate the virtual environment:
```sh
source .venv/bin/activate
```

Run the advisor script, which will connect to your Robinhood account:
```sh
make run
```

## Configuration

Update the `.env` file with your specific settings and Robinhood credentials. Here's an example configuration:

```
# ... [other configurations] ...

# Robinhood credentials
ROBINHOOD_USERNAME=your_email@example.com
ROBINHOOD_PASSWORD=your_secure_password

# ... [other configurations] ...
```

Ensure your Robinhood credentials are kept secure and never shared or committed to version control.

## Sample Output

Here's a sample output illustrating the tiered allocation and Robinhood-based investment advice:

```
Fetching current holdings from Robinhood...
Analyzing portfolio and comparing to target allocations...

Rank | Stock | Target Allocation | Current Allocation | Difference
---------------------------------------
   1 | IVV    |     19.34% |     18.50% |    -0.84%
   2 | XLV    |     15.47% |     16.20% |    +0.73%
   3 | AVUV   |     12.38% |     11.80% |    -0.58%
   ... [truncated for brevity] ...

Starting new investment allocation with $10000.00

Allocating to zero positions:
Allocated $33.25 to HAL (zero_position)
Allocated $69.70 to WMT (zero_position)
... [truncated for brevity] ...

Final allocation plan (based on current Robinhood holdings):
HAL: $178.83 (5 shares at $33.25 each)
WMT: $69.70 (1 share at $69.70 each)
... [truncated for brevity] ...

Remaining unallocated amount: $27.75

Robinhood API calls made: 15
```

This output demonstrates how the script analyzes your current Robinhood portfolio, compares it to your target allocations, and provides advice on new investments.

## Project Structure

```
.
├── Makefile
├── README.md
├── pyproject.toml
└── src
    └── advisor
        ├── __init__.py
        ├── allocate.py
        ├── main.py
        └── robinhood.py
```

- `src/advisor/main.py`: The main script that orchestrates the ETF allocation and Robinhood-based investment advice.
- `src/advisor/allocate.py`: Contains functions for stock allocation calculations.
- `src/advisor/robinhood.py`: Handles all interactions with the Robinhood API, including fetching holdings and prices.

## Development

To run the advisor and connect to Robinhood:
```sh
make run
```

To clean up generated files:
```sh
make clean
```

## Security Note

This project requires your Robinhood credentials to function. Always ensure that your `.env` file is secure and never commit it to version control. Use secure practices when handling your financial credentials.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This software is for educational purposes only. It is not intended to provide investment advice. Always consult with a qualified financial advisor before making investment decisions. Use of this software to interact with your Robinhood account is at your own risk.
