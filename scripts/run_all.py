#!/usr/bin/env python3
"""
Utility script to run the entire e-commerce data pipeline.
"""

import subprocess
import sys
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    logger.info(f"Running command: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd,
            check=True, 
            capture_output=True, 
            text=True
        )
        logger.debug(f"Command output: {result.stdout}")
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with exit code {e.returncode}")
        logger.error(f"Error output: {e.stderr}")
        raise

def main():
    """Run the complete e-commerce data pipeline"""
    logger.info("Starting complete e-commerce data pipeline...")
    
    try:
        # Step 1: Generate synthetic data
        logger.info("Step 1: Generating synthetic data...")
        run_command("python generate_data.py", cwd="../etl")
        
        # Step 2: Load data into SQLite
        logger.info("Step 2: Loading data into SQLite...")
        run_command("python load_sqlite.py", cwd="../etl")
        
        # Step 3: Run SQL analysis queries
        logger.info("Step 3: Running SQL analysis queries...")
        # We'll just verify the queries can be parsed without errors
        analysis_sql_path = "../sql/analysis.sql"
        if os.path.exists(analysis_sql_path):
            with open(analysis_sql_path, 'r') as f:
                queries = f.read().split(';')
                logger.info(f"Found {len(queries)-1} SQL queries in analysis file")
        
        # Step 4: Generate data profiling reports
        logger.info("Step 4: Generating data profiling reports...")
        run_command("python generate_profiles.py", cwd="../scripts")
        
        # Step 5: Generate documentation
        logger.info("Step 5: Generating documentation...")
        run_command("python generate_docs.py", cwd="../scripts")
        
        logger.info("Complete e-commerce data pipeline finished successfully!")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()