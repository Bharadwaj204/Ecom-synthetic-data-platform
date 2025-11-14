# E-commerce Data Engineering Pipeline - Enterprise-Grade Implementation Prompt

This is a comprehensive prompt template that contains all the necessary details to recreate the complete enterprise-grade e-commerce data engineering pipeline. Use this prompt with AI coding assistants to generate the entire project.

## Project Overview

Create a complete end-to-end mini data-engineering system for an e-commerce dataset with production-grade quality. The system should include:

1. Synthetic data generation with controlled randomness
2. Fully normalized relational data model with constraints
3. ETL pipeline into SQLite with validation
4. Data validation, logging, tests, and auto-generated documentation
5. SQL analysis queries for business insights
6. REST API for data access
7. Interactive dashboard for data visualization
8. Containerization with Docker
9. CI/CD pipeline ready for GitHub
10. Comprehensive documentation

## Technology Stack

- **Core**: Python 3.9+
- **Data Processing**: pandas, numpy, faker
- **Data Validation**: pandera
- **Data Profiling**: ydata-profiling
- **Database**: SQLite
- **API**: FastAPI
- **Dashboard**: Streamlit
- **Containerization**: Docker, docker-compose
- **Testing**: pytest
- **Build Automation**: Makefile
- **Documentation**: Auto-generated Markdown

## Project Structure

```
ecom_project/
├── .github/
│   └── workflows/
│       └── ci.yml
├── api/
│   └── main.py
├── dashboard/
│   └── app.py
├── data/
├── database/
├── docs/
│   └── profiling_reports/
├── etl/
│   ├── generate_data.py
│   └── load_sqlite.py
├── models/
│   └── schema.sql
├── scripts/
│   ├── generate_docs.py
│   ├── generate_profiles.py
│   └── run_all.py
├── sql/
│   └── analysis.sql
├── tests/
│   ├── test_data_generation.py
│   ├── test_etl.py
│   ├── test_api.py
│   └── test_dashboard.py
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── README.md
└── requirements.txt
```

## Component Requirements

### 1. Data Generation (`etl/generate_data.py`)

Create a Python script that generates 5 related e-commerce CSV datasets:

**Customers** (2,000 records):
- customer_id (int, unique)
- first_name (str)
- last_name (str)
- email (str, unique)
- signup_date (date)

**Products** (600 records):
- product_id (int, unique)
- name (str)
- category (str, from predefined list)
- price (float, > 0)

**Orders** (4,000 records):
- order_id (int, unique)
- customer_id (int, references customers)
- order_date (date)
- total_amount (float, >= 0)

**Order Items** (10,000 records):
- order_item_id (int, unique)
- order_id (int, references orders)
- product_id (int, references products)
- quantity (int, > 0)
- line_total (float, >= 0)

**Payments** (4,000 records):
- payment_id (int, unique)
- order_id (int, references orders)
- payment_method (str, from ['card', 'paypal', 'bank'])
- amount (float, >= 0)
- payment_date (date)

Requirements:
- Use controlled randomness (log-normal distributions for prices, Poisson for order volumes)
- Ensure referential integrity between all tables
- Implement comprehensive data validation with pandera schemas
- Save all files to the `data/` directory
- Include proper logging and error handling

### 2. Database Schema (`models/schema.sql`)

Create a fully normalized SQLite schema with:

- 5 tables: customers, products, orders, order_items, payments
- Primary keys for all tables
- Foreign key constraints with proper references
- NOT NULL constraints where appropriate
- CHECK constraints for data validation (e.g., price > 0)
- Indexes for performance on frequently queried columns
- Proper data types (INTEGER, TEXT, REAL, DATE)

### 3. ETL Pipeline (`etl/load_sqlite.py`)

Create a Python script that:

- Loads all 5 CSV files from the `data/` directory
- Creates the database schema from `models/schema.sql`
- Inserts data into SQLite database in the `database/` directory
- Implements chunked loading for memory efficiency
- Includes data validation during ingestion
- Provides comprehensive logging
- Handles errors gracefully

### 4. REST API (`api/main.py`)

Create a FastAPI application that provides:

- CRUD endpoints for all entities (customers, products, orders)
- Analytics endpoints for business insights
- Proper Pydantic models for request/response validation
- Health check endpoint
- Automatic OpenAPI documentation
- Proper error handling and HTTP status codes

Endpoints:
- GET /customers/ - List customers with optional filtering
- GET /customers/{id} - Get specific customer
- GET /products/ - List products with optional filtering
- GET /products/{id} - Get specific product
- GET /orders/ - List orders with optional filtering
- GET /orders/{id} - Get specific order
- GET /analytics/revenue/daily - Daily revenue summary
- GET /analytics/top-customers - Top customers by spend
- GET /analytics/top-products - Top products by revenue

### 5. Dashboard (`dashboard/app.py`)

Create a Streamlit application with:

- Multi-page interface (Overview, Customers, Products, Orders, Analytics)
- Interactive visualizations using Plotly
- Key metrics display
- Data exploration capabilities
- Business intelligence insights
- Responsive design

Pages:
- Overview: System metrics and recent orders
- Customers: Customer list and signup trends
- Products: Product list and category distribution
- Orders: Order list and trends
- Analytics: Revenue analysis and business insights

### 6. Data Profiling (`scripts/generate_profiles.py`)

Create a Python script that:

- Generates comprehensive profiling reports for all datasets using ydata-profiling
- Saves HTML reports to `docs/profiling_reports/`
- Includes statistical summaries, distributions, correlations
- Handles missing data analysis and duplicate detection
- Provides interactive visualizations

### 7. Documentation (`scripts/generate_docs.py`)

Create a Python script that:

- Generates a comprehensive data dictionary
- Includes entity relationship diagram
- Documents table schemas with constraints
- Shows foreign key relationships
- Provides column descriptions
- Saves to `docs/data_dictionary.md`

### 8. SQL Analysis (`sql/analysis.sql`)

Create SQL queries for:

- Top customers by spend
- Top products by revenue
- Revenue by category
- Revenue time series (daily, weekly, monthly)
- Average order value per customer
- Fraud-like anomalies detection
- Power user analysis

### 9. Testing (`tests/`)

Create comprehensive test suites:

- Data generation tests with pandera validation
- ETL pipeline tests for schema creation and data loading
- API endpoint tests
- Dashboard module tests
- Graceful handling of missing dependencies
- Proper test fixtures and setup/teardown

### 10. Docker Configuration

**Dockerfile**:
- Use Python 3.9 slim base image
- Install all dependencies
- Copy project files
- Expose necessary ports
- Set up working directory
- Include entry point for pipeline execution

**docker-compose.yml**:
- Multi-service orchestration (pipeline, API, dashboard)
- Volume mounting for data persistence
- Port exposure for services
- Environment variable configuration
- Service dependencies

### 11. Build Automation (`Makefile`)

Include commands for:
- setup - Install dependencies
- generate - Generate synthetic data
- ingest - Ingest data into database
- test - Run test suite
- docs - Generate documentation
- profile - Generate profiling reports
- api - Start REST API server
- dashboard - Start Streamlit dashboard
- run - Run complete pipeline
- clean - Clean generated files
- docker-build - Build Docker images
- docker-run - Run with Docker

### 12. CI/CD Pipeline (`.github/workflows/ci.yml`)

GitHub Actions workflow that includes:
- Dependency installation
- Code linting
- SQL syntax validation
- Test execution
- Schema validation testing
- Profiling report generation
- API and dashboard module testing
- Artifact upload

### 13. Requirements (`requirements.txt`)

Include all necessary Python packages:
- faker
- pandas
- numpy
- pytest
- rich
- sqlalchemy
- pydantic
- matplotlib
- ydata-profiling
- pandera
- fastapi
- uvicorn
- streamlit
- plotly

### 14. README.md

Comprehensive documentation including:
- Project overview
- Entity relationship diagram
- Project structure
- Quick start guide
- Usage instructions for all components
- Testing information
- API documentation
- Dashboard usage
- Data model details
- CI/CD pipeline information
- Requirements
- GitHub push instructions

## Quality Requirements

1. **Production-Grade Code**:
   - Proper error handling and logging
   - Type hints where appropriate
   - Comprehensive documentation
   - Consistent code style
   - Efficient algorithms and data structures

2. **Data Quality**:
   - Schema validation with pandera
   - Referential integrity enforcement
   - Data profiling for quality insights
   - Tolerance-based floating point comparisons
   - Comprehensive data validation

3. **Testing**:
   - High test coverage
   - Graceful dependency handling
   - Proper test fixtures
   - Clear test descriptions
   - Integration testing

4. **Security**:
   - Input validation
   - SQL injection prevention
   - Secure API practices
   - Proper error messaging

5. **Performance**:
   - Chunked data processing
   - Efficient database queries
   - Memory optimization
   - Caching where appropriate

6. **Maintainability**:
   - Modular design
   - Clear separation of concerns
   - Comprehensive documentation
   - Consistent naming conventions
   - Proper configuration management

## Implementation Guidelines

1. Use absolute paths for file operations to ensure consistency
2. Implement proper logging with both file and console output
3. Handle missing dependencies gracefully in test files
4. Use tolerance-based comparisons for floating-point values
5. Ensure all database operations are transactional
6. Validate data at every step of the pipeline
7. Provide meaningful error messages
8. Include comprehensive comments and docstrings
9. Follow Python best practices and PEP 8 style guide
10. Ensure cross-platform compatibility

This prompt provides all the necessary information to recreate the complete enterprise-grade e-commerce data engineering pipeline with all its components and features.