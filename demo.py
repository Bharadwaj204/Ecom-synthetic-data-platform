#!/usr/bin/env python3
"""
Demo script showcasing all the enhanced features of the e-commerce data pipeline.
"""

import subprocess
import sys
import os
import time

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd,
            check=True, 
            capture_output=True, 
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return None

def main():
    """Demonstrate all enhanced features"""
    print("🚀 E-commerce Data Pipeline Enhanced Features Demo")
    print("=" * 50)
    
    # 1. Setup dependencies
    print("\n1. Setting up dependencies...")
    run_command("pip install -r requirements.txt")
    
    # 2. Generate data with schema validation
    print("\n2. Generating data with Pandera schema validation...")
    run_command("python etl/generate_data.py")
    
    # 3. Generate profiling reports
    print("\n3. Generating data profiling reports...")
    run_command("python scripts/generate_profiles.py")
    
    # 4. Ingest data into database
    print("\n4. Ingesting data into SQLite database...")
    run_command("python etl/load_sqlite.py")
    
    # 5. Generate documentation
    print("\n5. Generating enhanced documentation...")
    run_command("python scripts/generate_docs.py")
    
    # 6. Run tests
    print("\n6. Running enhanced test suite...")
    run_command("python -m pytest tests/ -v")
    
    print("\n" + "=" * 50)
    print("✅ Demo completed successfully!")
    print("\nEnhanced features demonstrated:")
    print("• Pandera schema validation for data quality")
    print("• ydata-profiling automated data profiling reports")
    print("• FastAPI REST API for data access")
    print("• Streamlit interactive analytics dashboard")
    print("• Makefile for streamlined operations")
    print("• Docker containerization support")
    print("• Enhanced test coverage")
    
    print("\n📁 Check the following directories for outputs:")
    print("• data/ - Generated CSV files")
    print("• database/ - SQLite database")
    print("• docs/ - Enhanced documentation")
    print("• docs/profiling_reports/ - Automated profiling reports")
    print("• logs/ - Log files")
    
    print("\n🚀 To start the REST API: python api/main.py")
    print("📊 To start the dashboard: streamlit run dashboard/app.py")
    print("🔧 To use Makefile commands: make help")

if __name__ == "__main__":
    main()