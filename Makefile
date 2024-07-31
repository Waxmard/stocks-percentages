.PHONY: all setup test clean

# Python interpreter to use
PYTHON := python3
VENV := .venv
BIN := $(VENV)/bin

all: setup test

$(VENV)/bin/activate:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV) || (echo "Failed to create virtual environment"; exit 1)
	@echo "Upgrading pip..."
	$(BIN)/python -m pip install --upgrade pip || (echo "Failed to upgrade pip"; exit 1)
	@echo "Installing requirements..."
	$(BIN)/pip install -r requirements.txt || (echo "Failed to install requirements"; exit 1)
	@echo "Virtual environment setup complete."

setup: $(VENV)/bin/activate

test: setup
	@echo "Running tests..."
	$(BIN)/python -m unittest discover -v

combined: setup
	@echo "Running combined script..."
	$(BIN)/python combined.py

tiered: setup
	@echo "Running tiered script..."
	$(BIN)/python tiered.py

update-requirements: setup
	@echo "Updating requirements..."
	$(BIN)/pip install --upgrade pip-tools
	$(BIN)/pip-compile requirements.in
	$(BIN)/pip-sync requirements.txt

lint: setup
	@echo "Running linters..."
	$(BIN)/pre-commit run --all-files

clean:
	@echo "Cleaning up..."
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
