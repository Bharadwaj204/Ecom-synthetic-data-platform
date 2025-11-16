#!/bin/bash
# Setup script for Streamlit Cloud deployment

# Install base requirements
pip install -r requirements.txt

# Create database directory if it doesn't exist
mkdir -p ../database

echo "Setup complete. Make sure to run the data pipeline first to generate the database."