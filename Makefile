# Data Analyst Streamlit App - Makefile

# Configurable variables
PYTHON = python3
STREAMLIT_APP = main.py

.PHONY: help install pip-install run pip-run clean

help:
	@echo "=========================================================================="
	@echo "                 Data Analyst Streamlit App Control Tool                  "
	@echo "=========================================================================="
	@echo "Available commands:"
	@echo "  make install      - Install dependencies using 'uv' (recommended)"
	@echo "  make run          - Run the Streamlit application using 'uv'"
	@echo "  make clean        - Clean cached python files and temporary artifacts"
	@echo "=========================================================================="

install:
	@echo "Installing dependencies using 'uv'..."
	uv sync

run:
	@echo "Launching Streamlit application with 'uv'..."
	uv run streamlit run $(STREAMLIT_APP)

clean:
	@echo "Cleaning up python cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "Cleanup completed successfully!"
