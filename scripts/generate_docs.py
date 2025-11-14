#!/usr/bin/env python3
"""
Auto-generated documentation for e-commerce data model and dataset.
"""

import sqlite3
import pandas as pd
import os
from datetime import datetime

def get_table_info(conn, table_name):
    """Get table schema information"""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    return cursor.fetchall()

def get_row_count(conn, table_name):
    """Get row count for a table"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cursor.fetchone()[0]

def get_foreign_keys(conn, table_name):
    """Get foreign key information for a table"""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA foreign_key_list({table_name})")
    return cursor.fetchall()

def generate_data_dictionary(db_path="../database/ecom.db", output_path="../docs/data_dictionary.md"):
    """Generate data dictionary documentation"""
    
    # Create docs directory if it doesn't exist
    docs_dir = os.path.dirname(output_path)
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
    
    conn = sqlite3.connect(db_path)
    
    try:
        # Get list of tables
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Generate markdown content
        content = []
        content.append("# E-commerce Data Dictionary")
        content.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        content.append("")
        content.append("## Project Overview")
        content.append("")
        content.append("This is a synthetic e-commerce dataset with the following features:")
        content.append("")
        content.append("- **Data Generation**: Python scripts using Faker library with controlled randomness")
        content.append("- **Data Validation**: Schema validation using Pandera")
        content.append("- **Data Profiling**: Automated profiling reports using ydata-profiling")
        content.append("- **Database**: SQLite with full normalization and constraints")
        content.append("- **API**: REST API using FastAPI for data access")
        content.append("- **Dashboard**: Interactive analytics dashboard using Streamlit")
        content.append("- **Testing**: Pytest test suite with comprehensive coverage")
        content.append("- **CI/CD**: GitHub Actions workflow for automated testing")
        content.append("- **Documentation**: Auto-generated data dictionary and profiling reports")
        content.append("")
        content.append("---")
        content.append("")
        
        # Add ERD diagram (ASCII)
        content.append("## Entity Relationship Diagram")
        content.append("```")
        content.append("customers ──┬─────────────┐")
        content.append("            │             │")
        content.append("            ▼             ▼")
        content.append("          orders ──┬───► payments")
        content.append("                   │")
        content.append("                   ▼")
        content.append("              order_items ──► products")
        content.append("```")
        content.append("")
        
        # Document each table
        for table_name in tables:
            content.append(f"## {table_name.title()}")
            content.append("")
            
            # Table description
            descriptions = {
                "customers": "Customer information including personal details and signup date",
                "products": "Product catalog with pricing and categorization",
                "orders": "Order records with customer references and totals",
                "order_items": "Individual items within orders with quantities and pricing",
                "payments": "Payment records linked to orders with payment method details"
            }
            
            content.append(descriptions.get(table_name, f"Description for {table_name}"))
            content.append("")
            
            # Row count
            row_count = get_row_count(conn, table_name)
            content.append(f"**Row Count:** {row_count:,}")
            content.append("")
            
            # Table schema
            content.append("### Schema")
            content.append("| Column | Type | Constraints | Description |")
            content.append("|--------|------|-------------|-------------|")
            
            columns = get_table_info(conn, table_name)
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                not_null = "NOT NULL" if col[3] == 1 else ""
                pk = "PRIMARY KEY" if col[5] == 1 else ""
                constraints = []
                if not_null:
                    constraints.append(not_null)
                if pk:
                    constraints.append(pk)
                
                # Add CHECK constraints if they exist
                if col_name in ["price", "total_amount", "line_total", "amount", "quantity"]:
                    if col_name in ["price", "total_amount", "line_total", "amount"] and "price" in col_name or "amount" in col_name or "total" in col_name:
                        constraints.append("CHECK(>= 0)")
                    elif col_name == "quantity":
                        constraints.append("CHECK(> 0)")
                
                # Add UNIQUE constraint for email
                if col_name == "email":
                    constraints.append("UNIQUE")
                
                # Add payment method constraint
                if col_name == "payment_method":
                    constraints.append("CHECK(IN ('card','paypal','bank'))")
                
                constraint_str = ", ".join(constraints) if constraints else ""
                
                # Column descriptions
                descriptions = {
                    "customer_id": "Unique identifier for the customer",
                    "first_name": "Customer's first name",
                    "last_name": "Customer's last name",
                    "email": "Customer's email address (unique)",
                    "signup_date": "Date when customer registered",
                    "product_id": "Unique identifier for the product",
                    "name": "Product name",
                    "category": "Product category",
                    "price": "Product price (must be > 0)",
                    "order_id": "Unique identifier for the order",
                    "order_date": "Date when order was placed",
                    "total_amount": "Total amount for the order",
                    "order_item_id": "Unique identifier for the order item",
                    "quantity": "Quantity of product ordered (must be > 0)",
                    "line_total": "Total cost for this line item",
                    "payment_id": "Unique identifier for the payment",
                    "payment_method": "Method of payment (card, paypal, bank)",
                    "amount": "Payment amount",
                    "payment_date": "Date when payment was processed"
                }
                
                description = descriptions.get(col_name, "")
                
                content.append(f"| {col_name} | {col_type} | {constraint_str} | {description} |")
            
            content.append("")
            
            # Foreign keys
            fks = get_foreign_keys(conn, table_name)
            if fks:
                content.append("### Foreign Keys")
                content.append("| Column | References |")
                content.append("|--------|------------|")
                for fk in fks:
                    from_col = fk[3]
                    to_table = fk[2]
                    to_col = fk[4]
                    content.append(f"| {from_col} | {to_table}({to_col}) |")
                content.append("")
            
            content.append("---")
            content.append("")
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        
        print(f"Data dictionary generated successfully at {output_path}")
        
    finally:
        conn.close()

def main():
    """Main function to generate documentation"""
    print("Generating data dictionary documentation...")
    generate_data_dictionary()
    print("Documentation generation complete!")

if __name__ == "__main__":
    main()