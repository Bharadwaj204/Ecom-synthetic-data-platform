# Setup script for Windows deployment

# Install base requirements
pip install -r requirements.txt

# Create database directory if it doesn't exist
New-Item -ItemType Directory -Force -Path "..\database"

Write-Host "Setup complete. Make sure to run the data pipeline first to generate the database."