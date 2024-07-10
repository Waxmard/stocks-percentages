# Personal ETF Creator

This project allows you to create a personalized ETF (Exchange-Traded Fund) by allocating stocks from different lists with custom weightings. It uses a geometric allocation strategy to distribute investments across selected stocks.

## Features

- Define multiple stock lists with custom allocations
- Geometric allocation strategy for stock weighting
- Configurable maximum number of stocks and minimum dollar amount per stock
- Automated requirements management and virtual environment setup

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
