#!/usr/bin/env python3
"""
Utility functions for the dashboard to generate sample data
"""

import pandas as pd
import sqlite3
import logging
import os
import random
from datetime import datetime, timedelta
from faker import Faker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Faker
fake = Faker()
Faker.seed(42)
random.seed(42)

def generate_sample_customers(num_customers=100):
    """Generate sample customers data"""
    logger.info(f"Generating {num_customers} sample customers...")
    
    # Generate signup dates with uniform distribution over 1 year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    customers = []
    emails = set()
    
    for i in range(1, num_customers + 1):
        # Ensure unique email
        email = fake.email()
        while email in emails:
            email = fake.email()
        emails.add(email)
        
        signup_date = fake.date_between(start_date=start_date, end_date=end_date)
        
        customers.append({
            'customer_id': i,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': email,
            'signup_date': signup_date
        })
    
    df = pd.DataFrame(customers)
    logger.info(f"Generated {len(df)} sample customers")
    return df

def generate_sample_products(num_products=50):
    """Generate sample products"""
    logger.info(f"Generating {num_products} sample products...")
    
    categories = [
        'Electronics', 'Clothing', 'Home & Garden', 'Books', 
        'Sports', 'Beauty', 'Toys', 'Automotive', 'Jewelry', 'Health'
    ]
    
    products = []
    for i in range(1, num_products + 1):
        category = random.choice(categories)
        # Generate prices between $5 and $500
        price = round(random.uniform(5, 500), 2)
        
        products.append({
            'product_id': i,
            'name': fake.word().capitalize() + ' ' + fake.word().capitalize(),
            'category': category,
            'price': price
        })
    
    df = pd.DataFrame(products)
    logger.info(f"Generated {len(df)} sample products with price range ${df['price'].min():.2f} - ${df['price'].max():.2f}")
    return df

def generate_sample_orders(num_orders=200, num_customers=100):
    """Generate sample orders"""
    logger.info(f"Generating {num_orders} sample orders...")
    
    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()
    
    orders = []
    for i in range(1, num_orders + 1):
        customer_id = random.randint(1, num_customers)
        order_date = fake.date_between(start_date=start_date, end_date=end_date)
        
        # Random total amount between $10 and $1000
        total_amount = round(random.uniform(10, 1000), 2)
        
        orders.append({
            'order_id': i,
            'customer_id': customer_id,
            'order_date': order_date,
            'total_amount': total_amount
        })
    
    df = pd.DataFrame(orders)
    logger.info(f"Generated {len(df)} sample orders")
    return df

def generate_sample_order_items(num_items=500, num_orders=200, num_products=50):
    """Generate sample order items"""
    logger.info(f"Generating {num_items} sample order items...")
    
    order_items = []
    item_id = 1
    
    for i in range(num_items):
        order_id = random.randint(1, num_orders)
        product_id = random.randint(1, num_products)
        quantity = random.randint(1, 5)
        
        # Get a random price for the product (in a real scenario, this would come from the products table)
        price = round(random.uniform(5, 500), 2)
        line_total = round(quantity * price, 2)
        
        order_items.append({
            'order_item_id': item_id,
            'order_id': order_id,
            'product_id': product_id,
            'quantity': quantity,
            'line_total': line_total
        })
        item_id += 1
    
    df = pd.DataFrame(order_items)
    logger.info(f"Generated {len(df)} sample order items")
    return df

def generate_sample_payments(num_payments=200, num_orders=200):
    """Generate sample payments"""
    logger.info(f"Generating {num_payments} sample payments...")
    
    payment_methods = ['card', 'paypal', 'bank']
    
    payments = []
    for i in range(1, num_payments + 1):
        order_id = random.randint(1, num_orders)
        payment_method = random.choice(payment_methods)
        
        # Random amount between $10 and $1000
        amount = round(random.uniform(10, 1000), 2)
        payment_date = fake.date_between(start_date=datetime.now() - timedelta(days=365), end_date=datetime.now())
        
        payments.append({
            'payment_id': i,
            'order_id': order_id,
            'payment_method': payment_method,
            'amount': amount,
            'payment_date': payment_date
        })
    
    df = pd.DataFrame(payments)
    logger.info(f"Generated {len(df)} sample payments")
    return df

def create_sample_database_schema(conn):
    """Create database tables with simplified schema"""
    schema_sql = """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        signup_date DATE NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        order_date DATE NOT NULL,
        total_amount REAL NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    );
    
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        line_total REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (order_id),
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    );
    
    CREATE TABLE IF NOT EXISTS payments (
        payment_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        payment_method TEXT NOT NULL,
        amount REAL NOT NULL,
        payment_date DATE NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (order_id)
    );
    """
    
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    conn.commit()
    logger.info("Sample database schema created successfully")

def load_sample_data_to_database():
    """Generate sample data and load it into the database"""
    try:
        # Create directories if they don't exist
        os.makedirs("../data", exist_ok=True)
        os.makedirs("../database", exist_ok=True)
        os.makedirs("../logs", exist_ok=True)
        
        # Generate sample data
        customers_df = generate_sample_customers(100)
        products_df = generate_sample_products(50)
        orders_df = generate_sample_orders(200, 100)
        order_items_df = generate_sample_order_items(500, 200, 50)
        payments_df = generate_sample_payments(200, 200)
        
        # Save to CSV
        customers_df.to_csv("../data/customers.csv", index=False)
        products_df.to_csv("../data/products.csv", index=False)
        orders_df.to_csv("../data/orders.csv", index=False)
        order_items_df.to_csv("../data/order_items.csv", index=False)
        payments_df.to_csv("../data/payments.csv", index=False)
        
        # Connect to database
        db_path = "../database/ecom.db"
        conn = sqlite3.connect(db_path)
        logger.info(f"Connected to database: {db_path}")
        
        # Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON")
        
        # Create schema
        create_sample_database_schema(conn)
        
        # Load data into tables
        customers_df.to_sql('customers', conn, if_exists='append', index=False)
        products_df.to_sql('products', conn, if_exists='append', index=False)
        orders_df.to_sql('orders', conn, if_exists='append', index=False)
        order_items_df.to_sql('order_items', conn, if_exists='append', index=False)
        payments_df.to_sql('payments', conn, if_exists='append', index=False)
        
        conn.commit()
        conn.close()
        logger.info("Sample data loaded successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error loading sample data: {str(e)}")
        return False