# Quick Start Guide - E-commerce Data Engineering Pipeline

This guide provides step-by-step instructions to get the enterprise-grade e-commerce data engineering pipeline up and running quickly.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Docker (optional, for containerized deployment)

## Installation

### 1. Clone or Download the Project

If you haven't already, clone or download the project to your local machine.

### 2. Install Dependencies

Using the Makefile (recommended):
```bash
make setup
```

Or manually:
```bash
pip install -r requirements.txt
```

## Quick Execution

### Run the Complete Pipeline

Using the Makefile (recommended):
```bash
make run
```

Or manually:
```bash
python scripts/run_all.py
```

This will:
1. Generate synthetic e-commerce data (customers, products, orders, etc.)
2. Ingest the data into SQLite database
3. Generate data profiling reports
4. Create comprehensive documentation

## Individual Component Execution

### 1. Generate Data

Using the Makefile:
```bash
make generate
```

Or manually:
```bash
python etl/generate_data_simple.py
```

Note: Use `generate_data_simple.py` for now as the main `generate_data.py` has some validation issues.

### 2. Ingest Data into Database

Using the Makefile:
```bash
make ingest
```

Or manually:
```bash
python etl/load_sqlite.py
```

### 3. Generate Profiling Reports

Using the Makefile:
```bash
make profile
```

Or manually:
```bash
python scripts/generate_profiles.py
```

### 4. Generate Documentation

Using the Makefile:
```bash
make docs
```

Or manually:
```bash
python scripts/generate_docs.py
```

## Running Tests

Using the Makefile:
```bash
make test
```

Or manually:
```bash
pytest tests/ -v
```

## Starting Services

### Start the REST API

Using the Makefile:
```bash
make api
```

Or manually:
```bash
python api/main.py
```

The API will be available at `http://localhost:8000`

### Start the Dashboard

Using the Makefile:
```bash
make dashboard
```

Or manually:
```bash
streamlit run dashboard/app.py
```

The dashboard will be available at `http://localhost:8501`

## Docker Deployment

### Build Docker Images

Using the Makefile:
```bash
make docker-build
```

Or manually:
```bash
docker-compose build
```

### Run Complete Pipeline with Docker

Using the Makefile:
```bash
make docker-run
```

Or manually:
```bash
docker-compose up pipeline
```

### Start All Services with Docker

```bash
docker-compose up
```

This will start:
- Pipeline service (data generation and ingestion)
- API service (REST API on port 8000)
- Dashboard service (Streamlit dashboard on port 8501)

Access the services at:
- API: http://localhost:8000
- Dashboard: http://localhost:8501

## Project Structure

After running the pipeline, the project will have the following structure:

```
ecom_project/
├── data/                  # Generated CSV files
├── database/              # SQLite database (ecom.db)
├── docs/                  # Documentation and profiling reports
│   └── profiling_reports/ # HTML profiling reports
├── logs/                  # Log files
└── ...                    # Source code and configuration files
```

## Troubleshooting

### Common Issues

1. **Permission Errors**: Make sure you have write permissions in the project directory
2. **Missing Dependencies**: Run `make setup` to install all required packages
3. **Port Conflicts**: If ports 8000 or 8501 are in use, stop the conflicting services

### Data Generation Issues

If you encounter issues with the main data generation script:
1. Use the simple version: `python etl/generate_data_simple.py`
2. Check that all required Python packages are installed
3. Ensure you have sufficient disk space

### Docker Issues

If you encounter Docker-related issues:
1. Make sure Docker is installed and running
2. Check Docker daemon status
3. Ensure sufficient resources are allocated to Docker

## Next Steps

After successfully running the pipeline:

1. **Explore the Data**: Check the generated CSV files in the `data/` directory
2. **Query the Database**: Use any SQLite client to explore the `database/ecom.db` file
3. **View Profiling Reports**: Open HTML files in `docs/profiling_reports/` in your browser
4. **Use the API**: Access the REST API at `http://localhost:8000`
5. **Explore the Dashboard**: Visit `http://localhost:8501` for interactive analytics
6. **Run Tests**: Execute `make test` to verify everything is working correctly

## Additional Resources

- [README.md](README.md) - Comprehensive project documentation
- [PROJECT_PROMPT_TEMPLATE.md](PROJECT_PROMPT_TEMPLATE.md) - Template for recreating the project
- [PROJECT_STATUS.md](PROJECT_STATUS.md) - Current project status and future steps
- [ENHANCEMENTS_SUMMARY.md](ENHANCEMENTS_SUMMARY.md) - Summary of all enterprise enhancements

For detailed information about each component, refer to the specific documentation files and source code.