# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional system dependencies for profiling
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Expose ports for API and dashboard
EXPOSE 8000 8501

# Create directories that might be needed
RUN mkdir -p data database logs docs/profiling_reports

# Default command to run the complete pipeline
CMD ["python", "scripts/run_all.py"]