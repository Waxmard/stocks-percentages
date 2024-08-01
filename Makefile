PYTHON := python3.12
PIP := $(PYTHON) -m pip
VENV_DIR := .venv
VENV_ACTIVATE := $(VENV_DIR)/bin/activate
SRC_DIR := src/advisor

.PHONY: install run clean help

install:
	@echo "Checking for virtual environment..."
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv $(VENV_DIR); \
	fi
	@echo "Installing dependencies..."
	@. $(VENV_ACTIVATE) && $(PIP) install -e .
	@echo "\nVirtual environment is ready. To activate it, run:"
	@echo "source $(VENV_ACTIVATE)"
	@echo "\nAfter activating, you can use 'make run' to execute the script."

run:
	$(VENV_DIR)/bin/python $(SRC_DIR)/main.py

clean:
	@echo "Cleaning up..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf *.egg-info
	rm -rf build dist

help:
	@echo "Available targets:"
	@echo "  install  - Create virtual environment (if needed) and install project dependencies"
	@echo "  make run      : Run the advisor"
	@echo "  clean    - Clean up generated files"
	@echo "  help     - Show this help message"
