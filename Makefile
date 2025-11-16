# Makefile for e-commerce data pipeline

# Variables
PYTHON = python
PIP = pip
DATA_DIR = data
DB_DIR = database
LOGS_DIR = logs
DOCS_DIR = docs

# Default target
.PHONY: help
help:
	@echo "E-commerce Data Pipeline Makefile"
	@echo "Available commands:"
	@echo "  make setup          - Install dependencies"
	@echo "  make generate       - Generate synthetic data"
	@echo "  make ingest         - Ingest data into SQLite"
	@echo "  make test           - Run tests"
	@echo "  make docs           - Generate documentation"
	@echo "  make profile        - Generate data profiling reports (requires additional dependencies)"
	@echo "  make api            - Start REST API server"
	@echo "  make dashboard      - Start Streamlit dashboard"
	@echo "  make run            - Run complete pipeline"
	@echo "  make clean          - Clean generated files"
	@echo "  make docker-build   - Build Docker image"
	@echo "  make docker-run     - Run with Docker"

# Setup dependencies
.PHONY: setup
setup:
	$(PIP) install -r requirements.txt

# Setup profiling dependencies
.PHONY: setup-profile
setup-profile:
	$(PIP) install -r profiling_requirements.txt

# Generate synthetic data
.PHONY: generate
generate:
	$(PYTHON) etl/generate_data.py

# Ingest data into SQLite
.PHONY: ingest
ingest:
	$(PYTHON) etl/load_sqlite.py

# Run tests
.PHONY: test
test:
	$(PYTHON) -m pytest tests/ -v

# Generate documentation
.PHONY: docs
docs:
	$(PYTHON) scripts/generate_docs.py

# Generate data profiling reports
.PHONY: profile
profile:
	@echo "Installing profiling dependencies..."
	$(PIP) install -r profiling_requirements.txt
	$(PYTHON) scripts/generate_profiles.py

# Start REST API server
.PHONY: api
api:
	$(PYTHON) api/main.py

# Start Streamlit dashboard
.PHONY: dashboard
dashboard:
	$(PYTHON) -m streamlit run dashboard/app.py

# Run complete pipeline
.PHONY: run
run:
	$(PYTHON) scripts/run_all.py

# Clean generated files
.PHONY: clean
clean:
	rm -rf $(DATA_DIR)/*
	rm -rf $(DB_DIR)/*
	rm -rf $(LOGS_DIR)/*
	rm -rf $(DOCS_DIR)/profiling_reports/*
	@echo "Cleaned generated files"

# Docker commands (if Dockerfile exists)
.PHONY: docker-build
docker-build:
	@if [ -f Dockerfile ]; then \
		docker build -t ecom-pipeline .; \
	else \
		echo "Dockerfile not found. Skipping docker build."; \
	fi

.PHONY: docker-run
docker-run:
	@if [ -f Dockerfile ]; then \
		docker run -p 8000:8000 ecom-pipeline; \
	else \
		echo "Dockerfile not found. Skipping docker run."; \
	fi