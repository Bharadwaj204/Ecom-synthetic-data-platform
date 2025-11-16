# Deployment Guide

## Streamlit Cloud Deployment

To deploy the dashboard to Streamlit Cloud:

1. Fork this repository to your GitHub account
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app and select your forked repository
4. Set the main file path to `dashboard/app.py`
5. In the requirements section, add:
   ```
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

## Local Deployment

### Prerequisites
- Python 3.7+

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd ecom_project

# Install base dependencies
pip install -r requirements.txt
```

### Run the Complete Pipeline
```bash
# Generate data and load into database
python scripts/run_all.py
```

### Start Services
```bash
# Start the API (port 8000)
python api/main.py

# In another terminal, start the Dashboard (port 8501)
streamlit run dashboard/app.py
```

## Docker Deployment

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

## Profiling Reports (Optional)

To generate profiling reports, you need additional dependencies:

```bash
# Install profiling dependencies
pip install -r profiling_requirements.txt

# Generate profiling reports
python scripts/generate_profiles.py
```

Note: The profiling functionality requires the `htmlmin` package which may not be compatible with all Python versions. If you encounter issues, you can skip this step as it's optional.