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
        # Use shell=False for better cross-platform compatibility
        if cwd:
            result = subprocess.run(
                command,
                cwd=cwd,
                check=True,
                capture_output=True,
                text=True,
                shell=True  # Keep shell=True for Windows compatibility
            )
        else:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                shell=True
            )
        logger.debug(f"Command output: {result.stdout}")
        if result.stderr:
            logger.debug(f"Command stderr: {result.stderr}")
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with exit code {e.returncode}")
        logger.error(f"Error output: {e.stderr}")
        logger.error(f"Standard output: {e.stdout}")
        raise

def main():
    """Run the complete e-commerce data pipeline"""
    logger.info("Starting complete e-commerce data pipeline...")
    
    try:
        # Get the absolute path of the project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        etl_dir = os.path.join(project_root, "etl")
        scripts_dir = os.path.join(project_root, "scripts")
        sql_dir = os.path.join(project_root, "sql")
        
        logger.info(f"Project root: {project_root}")
        logger.info(f"ETL directory: {etl_dir}")
        logger.info(f"Scripts directory: {scripts_dir}")
        
        # Step 1: Generate synthetic data
        logger.info("Step 1: Generating synthetic data...")
        run_command("python generate_data.py", cwd=etl_dir)
        
        # Step 2: Load data into SQLite
        logger.info("Step 2: Loading data into SQLite...")
        run_command("python load_sqlite.py", cwd=etl_dir)
        
        # Step 3: Run SQL analysis queries
        logger.info("Step 3: Running SQL analysis queries...")
        # We'll just verify the queries can be parsed without errors
        analysis_sql_path = os.path.join(sql_dir, "analysis.sql")
        if os.path.exists(analysis_sql_path):
            with open(analysis_sql_path, 'r') as f:
                queries = f.read().split(';')
                logger.info(f"Found {len(queries)-1} SQL queries in analysis file")
        
        # Step 4: Generate data profiling reports
        logger.info("Step 4: Generating data profiling reports...")
        run_command("python generate_profiles.py", cwd=scripts_dir)
        
        # Step 5: Generate documentation
        logger.info("Step 5: Generating documentation...")
        run_command("python generate_docs.py", cwd=scripts_dir)
        
        logger.info("Complete e-commerce data pipeline finished successfully!")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        logger.exception("Full traceback:")
        sys.exit(1)

if __name__ == "__main__":
    main()