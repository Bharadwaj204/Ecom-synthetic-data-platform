#!/usr/bin/env python3
"""
Generate data profiling reports using ydata-profiling for all e-commerce datasets.
"""

import pandas as pd
import os
from ydata_profiling import ProfileReport
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_profile_report(df, title, output_path):
    """Generate a profile report for a dataframe"""
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
    profile.to_file(output_path)
    logger.info(f"Profile report saved to {output_path}")

def main():
    """Generate profiling reports for all e-commerce datasets"""
    logger.info("Starting data profiling report generation...")
    
    # Create profiling reports directory
    reports_dir = "../docs/profiling_reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        logger.info(f"Created directory: {reports_dir}")
    
    # Define data files and corresponding report titles
    data_files = [
        ("../data/customers.csv", "Customers Data Profile"),
        ("../data/products.csv", "Products Data Profile"),
        ("../data/orders.csv", "Orders Data Profile"),
        ("../data/order_items.csv", "Order Items Data Profile"),
        ("../data/payments.csv", "Payments Data Profile")
    ]
    
    # Generate profile reports for each dataset
    for file_path, title in data_files:
        try:
            if os.path.exists(file_path):
                logger.info(f"Loading data from {file_path}...")
                df = pd.read_csv(file_path)
                report_filename = os.path.splitext(os.path.basename(file_path))[0] + "_profile.html"
                report_path = os.path.join(reports_dir, report_filename)
                generate_profile_report(df, title, report_path)
            else:
                logger.warning(f"File not found: {file_path}")
        except Exception as e:
            logger.error(f"Error generating profile for {file_path}: {str(e)}")
    
    logger.info("Data profiling report generation completed!")

if __name__ == "__main__":
    main()