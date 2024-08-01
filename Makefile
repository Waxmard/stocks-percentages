.PHONY: all setup clean

# Python interpreter to use
PYTHON := python3
VENV := .venv
BIN := $(VENV)/bin

all: setup

$(VENV)/bin/activate:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV) || (echo "Failed to create virtual environment"; exit 1)
	@echo "Upgrading pip..."
	$(BIN)/python -m pip install --upgrade pip || (echo "Failed to upgrade pip"; exit 1)
	@echo "Installing project and dependencies..."
	$(BIN)/pip install -e ".[dev]" || (echo "Failed to install project and dependencies"; exit 1)
	@echo "Virtual environment setup complete."

setup: $(VENV)/bin/activate

run: setup
	@echo "Running tiered script..."
	$(BIN)/python tiered.py

update-dependencies: setup
	@echo "Updating dependencies..."
	$(BIN)/pip install --upgrade pip-tools
	$(BIN)/pip-compile pyproject.toml --output-file=requirements.txt
	$(BIN)/pip-sync requirements.txt

lint: setup
	@echo "Running linters..."
	$(BIN)/pre-commit run --all-files

clean:
	@echo "Cleaning up..."
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
