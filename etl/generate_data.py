#!/usr/bin/env python3
"""
Advanced synthetic e-commerce data generator with controlled randomness and constraint validation.
"""

import os
import logging
import random
from datetime import datetime, timedelta

# Set environment variable to disable pyarrow integration
os.environ['ARROW_PRE_0_15_IPC_FORMAT'] = '1'
os.environ['PYARROW_IGNORE_TIMEZONE'] = '1'

# Handle pandas import with pyarrow compatibility issue
try:
    import pandas as pd
    import numpy as np
    from scipy import stats
except ImportError as e:
    print(f"Error importing pandas/numpy: {e}")
    raise

try:
    from faker import Faker
except ImportError as e:
    print(f"Error importing faker: {e}")
    raise

try:
    import pandera as pa
    from pandera import Column, DataFrameSchema, Check
except ImportError as e:
    print(f"Error importing pandera: {e}")
    raise

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Faker
fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# Define data schemas using pandera
CUSTOMERS_SCHEMA = DataFrameSchema({
    "customer_id": Column(int, Check.greater_than(0), unique=True),
    "first_name": Column(str, Check.str_length(min_value=1)),
    "last_name": Column(str, Check.str_length(min_value=1)),
    "email": Column(str, Check.str_length(min_value=5), unique=True),
    "signup_date": Column(object)  # Using object type to avoid datetime conversion issues
})

PRODUCTS_SCHEMA = DataFrameSchema({
    "product_id": Column(int, Check.greater_than(0), unique=True),
    "name": Column(str, Check.str_length(min_value=1)),
    "category": Column(str, Check.isin([
        'Electronics', 'Clothing', 'Home & Garden', 'Books', 
        'Sports', 'Beauty', 'Toys', 'Automotive', 'Jewelry', 'Health'
    ])),
    "price": Column(float, Check.greater_than(0))
})

ORDERS_SCHEMA = DataFrameSchema({
    "order_id": Column(int, Check.greater_than(0), unique=True),
    "customer_id": Column(int, Check.greater_than(0)),
    "order_date": Column(object),  # Using object type to avoid datetime conversion issues
    "total_amount": Column(float, Check.greater_than_or_equal_to(0))
})

ORDER_ITEMS_SCHEMA = DataFrameSchema({
    "order_item_id": Column(int, Check.greater_than(0), unique=True),
    "order_id": Column(int, Check.greater_than(0)),
    "product_id": Column(int, Check.greater_than(0)),
    "quantity": Column(int, Check.greater_than(0)),
    "line_total": Column(float, Check.greater_than_or_equal_to(0))
})

PAYMENTS_SCHEMA = DataFrameSchema({
    "payment_id": Column(int, Check.greater_than(0), unique=True),
    "order_id": Column(int, Check.greater_than(0)),
    "payment_method": Column(str, Check.isin(['card', 'paypal', 'bank'])),
    "amount": Column(float, Check.greater_than_or_equal_to(0)),
    "payment_date": Column(object)  # Using object type to avoid datetime conversion issues
})

def generate_customers(num_customers=2000):
    """Generate synthetic customers data with uniform signup distribution"""
    logger.info(f"Generating {num_customers} customers...")
    
    # Generate signup dates with uniform distribution over 3 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3*365)
    
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
    # Validate schema
    df = CUSTOMERS_SCHEMA.validate(df)
    logger.info(f"Generated {len(df)} customers")
    return df

def generate_products(num_products=600):
    """Generate synthetic products with log-normal price distribution"""
    logger.info(f"Generating {num_products} products...")
    
    # Log-normal distribution for prices (more realistic for product prices)
    # Mean=3, sigma=1 gives us a good range of prices
    prices = np.random.lognormal(mean=3, sigma=1, size=num_products)
    prices = np.round(prices, 2)
    
    categories = [
        'Electronics', 'Clothing', 'Home & Garden', 'Books', 
        'Sports', 'Beauty', 'Toys', 'Automotive', 'Jewelry', 'Health'
    ]
    
    products = []
    for i in range(1, num_products + 1):
        category = random.choice(categories)
        price = max(0.01, prices[i-1])  # Ensure price > 0
        
        products.append({
            'product_id': i,
            'name': fake.word().capitalize() + ' ' + fake.word().capitalize(),
            'category': category,
            'price': price
        })
    
    df = pd.DataFrame(products)
    # Validate schema
    df = PRODUCTS_SCHEMA.validate(df)
    logger.info(f"Generated {len(df)} products with price range ${df['price'].min():.2f} - ${df['price'].max():.2f}")
    return df

def generate_orders(num_orders=4000, num_customers=2000, start_date=None, end_date=None):
    """Generate synthetic orders with Poisson distribution for order volume"""
    logger.info(f"Generating {num_orders} orders...")
    
    if not start_date:
        start_date = datetime.now() - timedelta(days=3*365)
    if not end_date:
        end_date = datetime.now()
    
    orders = []
    for i in range(1, num_orders + 1):
        customer_id = random.randint(1, num_customers)
        order_date = fake.date_between(start_date=start_date, end_date=end_date)
        
        # Initialize with 0, will be updated when order items are generated
        orders.append({
            'order_id': i,
            'customer_id': customer_id,
            'order_date': order_date,
            'total_amount': 0.0
        })
    
    df = pd.DataFrame(orders)
    # Validate schema
    df = ORDERS_SCHEMA.validate(df)
    logger.info(f"Generated {len(df)} orders")
    return df

def generate_order_items(orders_df, products_df, num_items=10000):
    """Generate synthetic order items with controlled randomness"""
    logger.info(f"Generating {num_items} order items...")
    
    order_items = []
    item_id = 1
    
    # Group orders by order_id for efficient processing
    orders_dict = orders_df.set_index('order_id').to_dict('index')
    
    # Ensure each order has at least one item
    order_ids = list(orders_dict.keys())
    for order_id in order_ids:
        # Select a random product
        product = products_df.sample(n=1).iloc[0]
        
        # Generate quantity (at least 1)
        quantity = random.randint(1, 3)
        line_total = round(quantity * product['price'], 2)
        
        order_items.append({
            'order_item_id': item_id,
            'order_id': order_id,
            'product_id': product['product_id'],
            'quantity': quantity,
            'line_total': line_total
        })
        
        # Update the order's total amount
        orders_dict[order_id]['total_amount'] += line_total
        item_id += 1
    
    # Generate remaining items randomly
    remaining_items = num_items - len(order_ids)
    for _ in range(remaining_items):
        # Select a random order
        order_id = random.choice(order_ids)
        order = orders_dict[order_id]
        
        # Select a random product
        product = products_df.sample(n=1).iloc[0]
        
        # Generate quantity with some distribution (mostly 1-3, occasionally higher)
        if random.random() < 0.7:
            quantity = random.randint(1, 3)
        else:
            quantity = random.randint(4, 10)
            
        line_total = round(quantity * product['price'], 2)
        
        order_items.append({
            'order_item_id': item_id,
            'order_id': order_id,
            'product_id': product['product_id'],
            'quantity': quantity,
            'line_total': line_total
        })
        
        # Update the order's total amount
        orders_dict[order_id]['total_amount'] += line_total
        item_id += 1
    
    # Update the orders dataframe with calculated totals
    for order_id, order_data in orders_dict.items():
        orders_df.loc[orders_df['order_id'] == order_id, 'total_amount'] = round(order_data['total_amount'], 2)
    
    df = pd.DataFrame(order_items)
    # Validate schema
    df = ORDER_ITEMS_SCHEMA.validate(df)
    logger.info(f"Generated {len(df)} order items")
    return df, orders_df

def generate_payments(orders_df):
    """Generate synthetic payments matching order totals"""
    logger.info(f"Generating {len(orders_df)} payments...")
    
    payment_methods = ['card', 'paypal', 'bank']
    payments = []
    
    for i, (_, order) in enumerate(orders_df.iterrows(), 1):
        payment_date = order['order_date'] + timedelta(days=random.randint(0, 7))
        payment_method = random.choice(payment_methods)
        
        payments.append({
            'payment_id': i,
            'order_id': order['order_id'],
            'payment_method': payment_method,
            'amount': order['total_amount'],
            'payment_date': payment_date
        })
    
    df = pd.DataFrame(payments)
    # Validate schema
    df = PAYMENTS_SCHEMA.validate(df)
    logger.info(f"Generated {len(df)} payments")
    return df

def validate_data(customers_df, products_df, orders_df, order_items_df, payments_df):
    """Validate all data constraints before saving"""
    logger.info("Validating data constraints...")
    
    # Validate customers
    assert customers_df['customer_id'].is_unique, "Customer IDs must be unique"
    assert customers_df['email'].is_unique, "Customer emails must be unique"
    assert not customers_df['first_name'].isnull().any(), "First names cannot be null"
    assert not customers_df['last_name'].isnull().any(), "Last names cannot be null"
    
    # Validate products
    assert products_df['product_id'].is_unique, "Product IDs must be unique"
    assert (products_df['price'] > 0).all(), "All prices must be > 0"
    assert not products_df['name'].isnull().any(), "Product names cannot be null"
    
    # Validate orders
    assert orders_df['order_id'].is_unique, "Order IDs must be unique"
    assert (orders_df['total_amount'] >= 0).all(), "All order totals must be >= 0"
    assert not orders_df['customer_id'].isnull().any(), "Customer IDs cannot be null"
    
    # Validate order items
    assert order_items_df['order_item_id'].is_unique, "Order item IDs must be unique"
    assert (order_items_df['quantity'] > 0).all(), "All quantities must be > 0"
    assert (order_items_df['line_total'] >= 0).all(), "All line totals must be >= 0"
    
    # Validate payments
    assert payments_df['payment_id'].is_unique, "Payment IDs must be unique"
    assert (payments_df['amount'] >= 0).all(), "All payment amounts must be >= 0"
    assert payments_df['payment_method'].isin(['card', 'paypal', 'bank']).all(), "Invalid payment methods"
    
    # Validate referential integrity
    assert orders_df['customer_id'].isin(customers_df['customer_id']).all(), "Orphaned customer IDs in orders"
    assert order_items_df['order_id'].isin(orders_df['order_id']).all(), "Orphaned order IDs in order items"
    assert order_items_df['product_id'].isin(products_df['product_id']).all(), "Orphaned product IDs in order items"
    assert payments_df['order_id'].isin(orders_df['order_id']).all(), "Orphaned order IDs in payments"
    
    # Validate order totals match sum of order items
    order_item_totals = order_items_df.groupby('order_id')['line_total'].sum().round(2)
    order_totals = orders_df.set_index('order_id')['total_amount'].round(2)
    # Debug output to see what's happening
    print(f"Order item totals count: {len(order_item_totals)}")
    print(f"Order totals count: {len(order_totals)}")
    # Check for mismatched orders
    mismatched = abs(order_item_totals - order_totals) >= 0.01
    if mismatched.any():
        print(f"Found {mismatched.sum()} mismatched orders")
        # Show first few mismatched orders
        mismatched_orders = order_item_totals[mismatched]
        for order_id in list(mismatched_orders.index)[:5]:
            item_total = order_item_totals[order_id]
            order_total = order_totals[order_id]
            print(f"Order {order_id}: item total={item_total}, order total={order_total}, diff={abs(item_total-order_total)}")
    # Use tolerance-based comparison for floating point comparison
    assert (abs(order_item_totals - order_totals) < 0.01).all(), "Order totals don't match sum of order items within tolerance"
    
    # Validate payment amounts match order totals
    payment_amounts = payments_df.set_index('order_id')['amount'].round(2)
    # Use tolerance-based comparison for floating point comparison
    assert (abs(order_totals - payment_amounts) < 0.01).all(), "Payment amounts don't match order totals within tolerance"
    
    logger.info("All data validations passed!")

def save_dataframes_to_csv(dataframes_dict, output_dir='../data'):
    """Save all dataframes to CSV files"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logger.info(f"Created directory: {output_dir}")
    
    for name, df in dataframes_dict.items():
        filename = f"{name}.csv"
        filepath = os.path.join(output_dir, filename)
        df.to_csv(filepath, index=False)
        logger.info(f"Saved {filename} with {len(df)} records")

def main():
    """Main function to generate all synthetic data"""
    print("Starting synthetic e-commerce data generation...")
    logger.info("Starting synthetic e-commerce data generation...")
    
    try:
        # Generate data
        print("Generating customers...")
        customers_df = generate_customers(2000)
        print("Generating products...")
        products_df = generate_products(600)
        print("Generating orders...")
        orders_df = generate_orders(4000, len(customers_df))
        print("Generating order items...")
        order_items_df, orders_df = generate_order_items(orders_df, products_df, 10000)
        print("Generating payments...")
        payments_df = generate_payments(orders_df)
        
        # Validate data
        print("Validating data...")
        validate_data(customers_df, products_df, orders_df, order_items_df, payments_df)
        
        # Display some statistics
        print(f"\nGenerated Data Statistics:")
        print(f"Customers: {len(customers_df):,}")
        print(f"Products: {len(products_df):,}")
        print(f"Orders: {len(orders_df):,}")
        print(f"Order Items: {len(order_items_df):,}")
        print(f"Payments: {len(payments_df):,}")
        logger.info(f"\nGenerated Data Statistics:")
        logger.info(f"Customers: {len(customers_df):,}")
        logger.info(f"Products: {len(products_df):,}")
        logger.info(f"Orders: {len(orders_df):,}")
        logger.info(f"Order Items: {len(order_items_df):,}")
        logger.info(f"Payments: {len(payments_df):,}")
        
        # Save to CSV files
        dataframes = {
            'customers': customers_df,
            'products': products_df,
            'orders': orders_df,
            'order_items': order_items_df,
            'payments': payments_df
        }
        
        print("Saving dataframes to CSV...")
        save_dataframes_to_csv(dataframes)
        print("\nData generation complete!")
        logger.info("\nData generation complete!")
        
    except Exception as e:
        print(f"Error during data generation: {str(e)}")
        logger.error(f"Error during data generation: {str(e)}")
        raise

if __name__ == "__main__":
    main()