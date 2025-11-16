import pandas as pd
import sqlite3
import logging
import os
from pathlib import Path
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("../logs/etl.log"),  # Fixed path to match original structure
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def setup_logging():
    """Setup logging directory and file"""
    log_dir = "../logs"  # Fixed path to match original structure
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return os.path.join(log_dir, "etl.log")

def create_database_schema(conn, schema_file="../models/schema.sql"):
    """Create database tables from schema file"""
    try:
        logger.info("Creating database schema...")
        # Use absolute path resolution
        schema_path = Path(schema_file).resolve()
        if not schema_path.exists():
            # Try alternative path
            schema_path = Path("models/schema.sql").resolve()
        if not schema_path.exists():
            # Try another alternative path
            schema_path = Path("../../models/schema.sql").resolve()
            
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found at {schema_file} or alternative paths")
            
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        cursor = conn.cursor()
        cursor.executescript(schema_sql)
        conn.commit()
        logger.info("Database schema created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating database schema: {str(e)}")
        return False

def load_csv_to_table(csv_file_path, table_name, conn, chunk_size=1000):
    """Load CSV data into SQLite table in chunks with validation"""
    try:
        # Try multiple possible paths
        possible_paths = [
            csv_file_path,
            f"../{csv_file_path}",
            f"../../{csv_file_path}"
        ]
        
        actual_path = None
        for path in possible_paths:
            if os.path.exists(path):
                actual_path = path
                break
                
        if actual_path is None:
            logger.warning(f"File not found at any of these locations: {possible_paths}")
            return False
        
        logger.info(f"Loading {actual_path} into {table_name} table...")
        
        # Read CSV in chunks
        chunk_count = 0
        total_rows = 0
        
        for chunk in pd.read_csv(actual_path, chunksize=chunk_size):
            chunk_count += 1
            rows_in_chunk = len(chunk)
            total_rows += rows_in_chunk
            
            # Validate data types
            # SQLite will handle type conversion, but we log the dtypes for reference
            logger.debug(f"Chunk {chunk_count} dtype info: {chunk.dtypes.to_dict()}")
            
            # Insert chunk into database
            chunk.to_sql(table_name, conn, if_exists='append', index=False)
            logger.debug(f"Inserted chunk {chunk_count} with {rows_in_chunk} rows")
        
        logger.info(f"Loaded {total_rows} rows into {table_name} table in {chunk_count} chunks")
        return True
        
    except Exception as e:
        logger.error(f"Error loading {csv_file_path} into {table_name}: {str(e)}")
        return False

def validate_data_integrity(conn):
    """Validate data integrity after loading"""
    try:
        logger.info("Validating data integrity...")
        cursor = conn.cursor()
        
        # Check row counts
        tables = ['customers', 'products', 'orders', 'order_items', 'payments']
        row_counts = {}
        
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            row_counts[table] = count
            logger.info(f"- {table}: {count:,} records")
        
        # Validate foreign key constraints by checking for orphaned records
        # This is a simplified check - in production, you'd rely on SQLite's FK enforcement
        cursor.execute("""
            SELECT COUNT(*) FROM orders o
            LEFT JOIN customers c ON o.customer_id = c.customer_id
            WHERE c.customer_id IS NULL
        """)
        orphaned_orders = cursor.fetchone()[0]
        if orphaned_orders > 0:
            logger.warning(f"Found {orphaned_orders} orders with invalid customer_id")
        
        cursor.execute("""
            SELECT COUNT(*) FROM order_items oi
            LEFT JOIN orders o ON oi.order_id = o.order_id
            LEFT JOIN products p ON oi.product_id = p.product_id
            WHERE o.order_id IS NULL OR p.product_id IS NULL
        """)
        orphaned_items = cursor.fetchone()[0]
        if orphaned_items > 0:
            logger.warning(f"Found {orphaned_items} order_items with invalid foreign keys")
        
        cursor.execute("""
            SELECT COUNT(*) FROM payments p
            LEFT JOIN orders o ON p.order_id = o.order_id
            WHERE o.order_id IS NULL
        """)
        orphaned_payments = cursor.fetchone()[0]
        if orphaned_payments > 0:
            logger.warning(f"Found {orphaned_payments} payments with invalid order_id")
        
        # Validate that order totals match sum of order items
        cursor.execute("""
            SELECT COUNT(*) FROM (
                SELECT o.order_id, o.total_amount, COALESCE(SUM(oi.line_total), 0) as items_total
                FROM orders o
                LEFT JOIN order_items oi ON o.order_id = oi.order_id
                GROUP BY o.order_id, o.total_amount
                HAVING ROUND(o.total_amount, 2) != ROUND(COALESCE(SUM(oi.line_total), 0), 2)
            )
        """)
        mismatched_orders = cursor.fetchone()[0]
        if mismatched_orders > 0:
            logger.warning(f"Found {mismatched_orders} orders with mismatched totals")
        else:
            logger.info("All order totals match sum of order items")
        
        # Validate that payment amounts match order totals
        cursor.execute("""
            SELECT COUNT(*) FROM (
                SELECT o.order_id, o.total_amount, p.amount
                FROM orders o
                JOIN payments p ON o.order_id = p.order_id
                WHERE ROUND(o.total_amount, 2) != ROUND(p.amount, 2)
            )
        """)
        mismatched_payments = cursor.fetchone()[0]
        if mismatched_payments > 0:
            logger.warning(f"Found {mismatched_payments} payments with mismatched amounts")
        else:
            logger.info("All payment amounts match order totals")
        
        logger.info("Data integrity validation completed")
        return row_counts
        
    except Exception as e:
        logger.error(f"Error during data integrity validation: {str(e)}")
        return {}

def main():
    """Main ETL function"""
    logger.info("Starting ETL pipeline...")
    
    # Setup logging
    log_file = setup_logging()
    logger.info(f"Logging to file: {log_file}")
    
    # Database connection
    db_path = "../database/ecom.db"  # Fixed path to match original structure
    conn = None
    
    try:
        # Create database directory if it doesn't exist
        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            logger.info(f"Created database directory: {db_dir}")
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        logger.info(f"Connected to database: {db_path}")
        
        # Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON")
        
        # Create schema
        if not create_database_schema(conn):
            raise Exception("Failed to create database schema")
        
        # Define CSV files and corresponding table names
        csv_files_and_tables = [
            ('data/customers.csv', 'customers'),  # Will look in multiple locations
            ('data/products.csv', 'products'),    # Will look in multiple locations
            ('data/orders.csv', 'orders'),        # Will look in multiple locations
            ('data/order_items.csv', 'order_items'),  # Will look in multiple locations
            ('data/payments.csv', 'payments')     # Will look in multiple locations
        ]
        
        # Load each CSV file into its corresponding table
        for csv_file, table_name in csv_files_and_tables:
            if not load_csv_to_table(csv_file, table_name, conn):
                logger.warning(f"Failed to load {csv_file} into {table_name}")
        
        # Validate data integrity
        row_counts = validate_data_integrity(conn)
        
        if row_counts:
            logger.info("ETL pipeline completed successfully!")
            return True
        else:
            logger.error("ETL pipeline completed with validation errors")
            return False
        
    except Exception as e:
        logger.error(f"Error during ETL pipeline: {str(e)}")
        return False
        
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)