# E-commerce Synthetic Data Platform

A complete end-to-end data engineering pipeline that generates synthetic e-commerce data, processes it through an ETL pipeline, stores it in a database, and provides analytics through an API and dashboard.

## 🏗️ Architecture

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
├── dashboard/         # Streamlit analytics dashboard
├── data/              # Generated CSV files (created during execution)
├── database/          # SQLite database (created during execution)
├── docs/              # Auto-generated documentation
│   └── profiling_reports/  # Data profiling reports (created during execution)
├── etl/               # ETL pipeline scripts
├── models/            # Data models and schema
├── scripts/           # Utility scripts
├── sql/               # SQL analysis queries
├── tests/             # Test suite
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Service orchestration
├── Makefile           # Build automation
├── README.md          # This file
└── requirements.txt   # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7-3.12 (Note: Python 3.13+ may have compatibility issues with some dependencies)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd ecom_project

# Install dependencies
pip install -r requirements.txt
```

### Run the Complete Pipeline
```bash
# Option 1: Using Makefile (recommended)
make run

# Option 2: Using Python script
python scripts/run_all.py
```

### Start Services
```bash
# Start the API
make api
# or
python api/main.py

# Start the Dashboard
make dashboard
# or
streamlit run dashboard/app.py
```

## 📊 Dashboard Deployment

To deploy the dashboard to Streamlit Cloud:

1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app and select your forked repository
4. Set the main file path to `dashboard/app.py`
5. Add the following to your app configuration:
   ```
   # Streamlit Cloud requirements
   faker
   pandas
   numpy
   pytest
   rich
   sqlalchemy
   pydantic
   matplotlib
   pandera
   fastapi
   uvicorn
   streamlit
   plotly
   ```

## 🛠️ Makefile Commands

```bash
make setup     # Install dependencies
make generate  # Generate synthetic data
make ingest    # Load data into SQLite
make test      # Run tests
make docs      # Generate documentation
make profile   # Generate profiling reports (requires additional dependencies)
make api       # Start FastAPI server
make dashboard # Launch Streamlit app
make run       # Full pipeline execution
make clean     # Remove generated files
```

## 🐳 Docker Deployment

```bash
# Build and run the complete pipeline
docker-compose up pipeline

# Start all services (API, Dashboard, and Pipeline)
docker-compose up

# Build images separately
docker-compose build

# Run specific services
docker-compose up api
docker-compose up dashboard
```

## 🔧 Technology Stack

- **Data Generation**: faker, pandas, numpy
- **Data Validation**: pandera
- **ETL & Database**: sqlite3
- **API**: FastAPI, uvicorn
- **Dashboard**: Streamlit, plotly, matplotlib
- **Profiling**: ydata-profiling (optional, for advanced analytics)
- **Testing**: pytest
- **Containerization**: Docker, docker-compose
- **Build Automation**: Makefile
- **CI/CD**: GitHub Actions

## 📈 Features

1. **Synthetic Data Generation**
   - Realistic customer profiles with Faker
   - Product catalog with categories and pricing
   - Order history with timestamps
   - Payment records with processing dates
   - Referential integrity between related entities

2. **ETL Pipeline**
   - CSV data loading with pandas
   - Schema validation with pandera
   - SQLite database with 3NF design
   - Data integrity checks and validation
   - Batch processing for large datasets

3. **REST API**
   - FastAPI with automatic OpenAPI documentation
   - CRUD operations for all entities
   - Health check endpoints
   - JSON data serialization

4. **Analytics Dashboard**
   - Streamlit web interface
   - Interactive visualizations with Plotly
   - Real-time data from SQLite
   - Multiple views (Overview, Customers, Products, Orders, Analytics)

5. **Data Profiling**
   - Automated data quality reports
   - Statistical analysis of all datasets
   - HTML reports for easy sharing
   - Data dictionary documentation

6. **Testing**
   - Unit tests for all components
   - Integration tests for ETL pipeline
   - API endpoint validation
   - Data validation tests

7. **Documentation**
   - Auto-generated data dictionary
   - Profiling reports for each dataset
   - API documentation via FastAPI
   - Comprehensive README

## 🧪 Testing

```bash
# Run all tests
make test
# or
python -m pytest tests/ -v
```

## 📚 API Documentation

Once the API is running, visit:
- http://localhost:8000/docs - Interactive API documentation
- http://localhost:8000/redoc - Alternative API documentation

## 🖥️ Dashboard

Once the dashboard is running, visit:
- http://localhost:8501 - Streamlit dashboard

## 📖 Data Dictionary

After running the pipeline, check `docs/data_dictionary.md` for detailed information about the database schema and field descriptions.

## 📊 Profiling Reports

To generate profiling reports (requires additional dependencies):
```bash
make profile
# or
pip install -r profiling_requirements.txt
python scripts/generate_profiles.py
```

Reports will be available in `docs/profiling_reports/`.

## ⚠️ Compatibility Notes

- **Python 3.13+**: Some dependencies like `htmlmin` (used by `ydata-profiling`) are not compatible with Python 3.13 due to the removal of the `cgi` module. For full functionality, use Python 3.7-3.12.
- **Streamlit Cloud**: The dashboard can be deployed to Streamlit Cloud without profiling dependencies.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.