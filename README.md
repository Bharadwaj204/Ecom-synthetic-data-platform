# E-commerce Data Engineering Pipeline

A complete end-to-end mini data-engineering system for an e-commerce dataset with production-grade quality.

## 🌟 Overview

This project provides a comprehensive data engineering pipeline that:

- Generates synthetic e-commerce datasets with controlled randomness
- Defines a clean, normalized relational data model
- Implements an ETL pipeline into SQLite with validation
- Includes data validation using Pandera schemas
- Provides automated data profiling reports using ydata-profiling
- Includes data validation, logging, tests, and auto-generated documentation
- Provides SQL analysis queries for business insights
- Offers REST API access using FastAPI
- Includes interactive analytics dashboard using Streamlit
- Is ready for GitHub with CI pipeline and comprehensive documentation
- Supports containerization with Docker

## 📊 Entity Relationship Diagram

```
customers ──┬─────────────┐
            │             │
            ▼             ▼
          orders ──┬───► payments
                   │
                   ▼
              order_items ──► products
```

## 📁 Project Structure

```
ecom_project/
├── api/               # REST API using FastAPI
│   └── main.py
├── dashboard/         # Streamlit analytics dashboard
│   └── app.py
├── data/              # Generated CSV files
├── database/          # SQLite database
├── docs/              # Auto-generated documentation
│   └── profiling_reports/  # Data profiling reports
├── etl/               # ETL pipeline scripts
│   ├── generate_data.py
│   └── load_sqlite.py
├── models/            # Data models and schema
│   └── schema.sql
├── scripts/           # Utility scripts
│   ├── generate_docs.py
│   ├── generate_profiles.py
│   └── run_all.py
├── sql/               # SQL analysis queries
│   └── analysis.sql
├── tests/             # Test suite
│   ├── test_data_generation.py
│   └── test_etl.py
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Service orchestration
├── Makefile           # Build automation
├── README.md
└── requirements.txt
```

## 🚀 Quick Start

### 1. Setup

```bash
# Clone the repository
git clone <repository-url>
cd ecom_project

# Install dependencies
pip install -r requirements.txt
```

### 2. Using Makefile (Recommended)

The project includes a Makefile for streamlined operations:

```bash
# Install dependencies
make setup

# Generate data
make generate

# Ingest data into database
make ingest

# Run complete pipeline
make run

# Generate profiling reports
make profile

# Generate documentation
make docs

# Run tests
make test

# Start REST API
make api

# Start Streamlit dashboard
make dashboard

# Clean generated files
make clean
```

### 2. Run the Complete Pipeline

```bash
# Run the entire pipeline with one command
python scripts/run_all.py
```

This will:
1. Generate synthetic data (2,000 customers, 600 products, 4,000 orders, etc.)
2. Load data into SQLite database
3. Run SQL analysis queries
4. Generate documentation

### 3. Individual Steps

#### Generate Data
```bash
cd etl
python generate_data.py
```

#### Load into SQLite
```bash
cd etl
python load_sqlite.py
```

#### Run Analysis Queries
```bash
# Use any SQLite client to run queries from sql/analysis.sql
# Or examine the file directly
cat sql/analysis.sql
```

#### Generate Documentation
```bash
cd scripts
python generate_docs.py
```

### 4. Using Docker

The project supports containerization with Docker:

```bash
# Build the Docker image
make docker-build
# or
docker-compose build

# Run the complete pipeline
make docker-run
# or
docker-compose up pipeline

# Start all services (pipeline, API, dashboard)
docker-compose up

# Start specific services
docker-compose up api         # REST API on port 8000
docker-compose up dashboard   # Streamlit dashboard on port 8501
```

## 🧪 Testing

Run the test suite:

```bash
# Install pytest if not already installed
pip install pytest

# Run all tests
pytest tests/ -v
```

## 📈 SQL Analysis Queries

The project includes several analytical SQL queries in `sql/analysis.sql`:

1. **Top 50 customers by spend**
2. **Top products by revenue**
3. **Revenue by category**
4. **Revenue time series** (daily, weekly, monthly)
5. **Average order value per customer**
6. **Fraud-like anomalies** (orders with mismatched payments)
7. **Power user analysis** (customers with > 90th percentile order volume)

## 🌐 REST API

The project includes a FastAPI-based REST API for programmatic access to the data:

- **Customers**: `/customers/`, `/customers/{id}`
- **Products**: `/products/`, `/products/{id}`
- **Orders**: `/orders/`, `/orders/{id}`
- **Analytics**: `/analytics/revenue/daily`, `/analytics/top-customers`, `/analytics/top-products`

Start the API with `make api` or `python api/main.py`, then access at `http://localhost:8000`.

## 📊 Streamlit Dashboard

The project includes an interactive analytics dashboard built with Streamlit:

- Overview of system metrics
- Customer analytics
- Product analytics
- Order analytics
- Business intelligence visualizations

Start the dashboard with `make dashboard` or `streamlit run dashboard/app.py`, then access at `http://localhost:8501`.

## 🛠️ Data Model

The database schema is fully normalized to 3NF with:

- **Customers**: customer information
- **Products**: product catalog
- **Orders**: order records
- **Order Items**: individual items within orders
- **Payments**: payment records

All tables have appropriate constraints, foreign keys, and indexes for performance.

## 📚 Documentation

Auto-generated documentation is available in `docs/data_dictionary.md` after running the pipeline.

## 🔄 CI/CD Pipeline

GitHub Actions workflow includes:

- Dependency installation
- Code linting with flake8
- SQL syntax validation
- Test execution
- Artifact upload

## 📦 Requirements

- Python 3.7+
- See `requirements.txt` for Python package dependencies

New dependencies for enhanced features:
- **ydata-profiling**: For automated data profiling reports
- **pandera**: For data schema validation
- **fastapi**: For REST API functionality
- **uvicorn**: For API server
- **streamlit**: For interactive dashboard
- **plotly**: For dashboard visualizations

## 📤 Push to GitHub

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: E-commerce data engineering pipeline"

# Add remote origin (replace with your repository URL)
git remote add origin https://github.com/your-username/ecom-project.git

# Push to GitHub
git push -u origin main
```"# Ecom-synthetic-data-platform" 
