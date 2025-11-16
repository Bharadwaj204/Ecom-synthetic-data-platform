#!/usr/bin/env python3
"""
Generate data profiling reports for all datasets using ydata-profiling.
This script is optional and requires additional dependencies.
"""

import pandas as pd
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_profiling_dependencies():
    """Check if profiling dependencies are available"""
    try:
        from ydata_profiling import ProfileReport
        return True
    except ImportError as e:
        logger.error(f"Profiling dependencies not available: {e}")
        logger.info("To install profiling dependencies, run: pip install -r profiling_requirements.txt")
        return False

def main():
    """Generate profiling reports for all datasets"""
    # Check if profiling dependencies are available
    if not check_profiling_dependencies():
        logger.error("Cannot generate profiling reports due to missing dependencies")
        sys.exit(1)
    
    from ydata_profiling import ProfileReport
    
    logger.info("Starting data profiling report generation...")
    
    # Create profiling reports directory
    reports_dir = "../docs/profiling_reports"
    os.makedirs(reports_dir, exist_ok=True)
    logger.info(f"Created directory: {reports_dir}")
    
    # Define datasets to profile
    datasets = [
        ("../data/customers.csv", "Customers Data Profile"),
        ("../data/products.csv", "Products Data Profile"),
        ("../data/orders.csv", "Orders Data Profile"),
        ("../data/order_items.csv", "Order Items Data Profile"),
        ("../data/payments.csv", "Payments Data Profile")
    ]
    
    # Generate profile report for each dataset
    for csv_path, title in datasets:
        if os.path.exists(csv_path):
            logger.info(f"Loading data from {csv_path}...")
            df = pd.read_csv(csv_path)
            
            logger.info(f"Generating profile report for {title}...")
            # Generate profile report
            # Remove dark_mode parameter which is no longer supported
            profile = ProfileReport(
                df, 
                title=title,
                explorative=True
                # dark_mode parameter removed as it's no longer supported
            )
            
            # Save report
            output_path = os.path.join(reports_dir, f"{title.lower().replace(' ', '_')}.html")
            profile.to_file(output_path)
            logger.info(f"Saved profile report to {output_path}")
        else:
            logger.warning(f"CSV file not found: {csv_path}")
    
    logger.info("Data profiling reports generation completed!")

if __name__ == "__main__":
    main()