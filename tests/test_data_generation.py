#!/usr/bin/env python3
"""
Test suite for data generation functionality.
"""

import sys
import os

# Add the etl directory to the path so we can import the generate_data module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'etl'))

# Conditional imports to handle missing dependencies
try:
    import pandas as pd
    import pytest
    from generate_data import generate_customers, generate_products, generate_orders, generate_order_items, generate_payments
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    # Create mock objects for when dependencies are not available
    pd = None
    pytest = None
    generate_customers = generate_products = generate_orders = generate_order_items = generate_payments = None
    DEPENDENCIES_AVAILABLE = False

def test_customer_generation():
    """Test that customer generation produces valid data"""
    if not DEPENDENCIES_AVAILABLE:
        pytest.skip("Dependencies not available")
    
    customers_df = generate_customers(100)
    
    # Check that we have the expected number of customers
    assert len(customers_df) == 100
    
    # Check that all required columns are present
    required_columns = ['customer_id', 'first_name', 'last_name', 'email', 'signup_date']
    for col in required_columns:
        assert col in customers_df.columns
    
    # Check that customer IDs are unique
    assert customers_df['customer_id'].is_unique
    
    # Check that emails are unique
    assert customers_df['email'].is_unique
    
    # Check that no fields are null
    assert not customers_df['first_name'].isnull().any()
    assert not customers_df['last_name'].isnull().any()
    assert not customers_df['email'].isnull().any()
    assert not customers_df['signup_date'].isnull().any()

def test_product_generation():
    """Test that product generation produces valid data"""
    if not DEPENDENCIES_AVAILABLE:
        pytest.skip("Dependencies not available")
    
    products_df = generate_products(50)
    
    # Check that we have the expected number of products
    assert len(products_df) == 50
    
    # Check that all required columns are present
    required_columns = ['product_id', 'name', 'category', 'price']
    for col in required_columns:
        assert col in products_df.columns
    
    # Check that product IDs are unique
    assert products_df['product_id'].is_unique
    
    # Check that prices are all greater than 0
    assert (products_df['price'] > 0).all()
    
    # Check that no fields are null
    assert not products_df['name'].isnull().any()
    assert not products_df['category'].isnull().any()
    assert not products_df['price'].isnull().any()

def test_order_generation():
    """Test that order generation produces valid data"""
    if not DEPENDENCIES_AVAILABLE:
        pytest.skip("Dependencies not available")
    
    orders_df = generate_orders(50, 100)
    
    # Check that we have the expected number of orders
    assert len(orders_df) == 50
    
    # Check that all required columns are present
    required_columns = ['order_id', 'customer_id', 'order_date', 'total_amount']
    for col in required_columns:
        assert col in orders_df.columns
    
    # Check that order IDs are unique
    assert orders_df['order_id'].is_unique
    
    # Check that total amounts are all greater than or equal to 0
    assert (orders_df['total_amount'] >= 0).all()
    
    # Check that customer IDs are within expected range
    assert (orders_df['customer_id'] >= 1).all()
    assert (orders_df['customer_id'] <= 100).all()
    
    # Check that no fields are null
    assert not orders_df['customer_id'].isnull().any()
    assert not orders_df['order_date'].isnull().any()

def test_order_item_generation():
    """Test that order item generation produces valid data"""
    if not DEPENDENCIES_AVAILABLE:
        pytest.skip("Dependencies not available")
    
    # First generate some test data
    customers_df = generate_customers(10)
    products_df = generate_products(20)
    orders_df = generate_orders(15, len(customers_df))
    
    # Generate order items
    order_items_df, updated_orders_df = generate_order_items(orders_df, products_df, 50)
    
    # Check that we have the expected number of order items
    assert len(order_items_df) == 50
    
    # Check that all required columns are present
    required_columns = ['order_item_id', 'order_id', 'product_id', 'quantity', 'line_total']
    for col in required_columns:
        assert col in order_items_df.columns
    
    # Check that order item IDs are unique
    assert order_items_df['order_item_id'].is_unique
    
    # Check that quantities are all greater than 0
    assert (order_items_df['quantity'] > 0).all()
    
    # Check that line totals are all greater than or equal to 0
    assert (order_items_df['line_total'] >= 0).all()
    
    # Check that order IDs reference existing orders
    assert order_items_df['order_id'].isin(orders_df['order_id']).all()
    
    # Check that product IDs reference existing products
    assert order_items_df['product_id'].isin(products_df['product_id']).all()
    
    # Check that no fields are null
    assert not order_items_df['order_id'].isnull().any()
    assert not order_items_df['product_id'].isnull().any()
    assert not order_items_df['quantity'].isnull().any()
    assert not order_items_df['line_total'].isnull().any()

def test_payment_generation():
    """Test that payment generation produces valid data"""
    if not DEPENDENCIES_AVAILABLE:
        pytest.skip("Dependencies not available")
    
    # First generate some test data
    customers_df = generate_customers(10)
    products_df = generate_products(20)
    orders_df = generate_orders(15, len(customers_df))
    order_items_df, orders_df = generate_order_items(orders_df, products_df, 30)
    
    # Generate payments
    payments_df = generate_payments(orders_df)
    
    # Check that we have the expected number of payments
    assert len(payments_df) == len(orders_df)
    
    # Check that all required columns are present
    required_columns = ['payment_id', 'order_id', 'payment_method', 'amount', 'payment_date']
    for col in required_columns:
        assert col in payments_df.columns
    
    # Check that payment IDs are unique
    assert payments_df['payment_id'].is_unique
    
    # Check that amounts are all greater than or equal to 0
    assert (payments_df['amount'] >= 0).all()
    
    # Check that payment methods are valid
    valid_methods = ['card', 'paypal', 'bank']
    assert payments_df['payment_method'].isin(valid_methods).all()
    
    # Check that order IDs reference existing orders
    assert payments_df['order_id'].isin(orders_df['order_id']).all()
    
    # Check that amounts match order totals
    order_amounts = orders_df.set_index('order_id')['total_amount']
    payment_amounts = payments_df.set_index('order_id')['amount']
    # Set the same name for both series to avoid assertion error
    order_amounts.name = 'amount'
    payment_amounts.name = 'amount'
    pd.testing.assert_series_equal(order_amounts, payment_amounts)
    
    # Check that no fields are null
    assert not payments_df['order_id'].isnull().any()
    assert not payments_df['payment_method'].isnull().any()
    assert not payments_df['amount'].isnull().any()
    assert not payments_df['payment_date'].isnull().any()

if __name__ == "__main__":
    if DEPENDENCIES_AVAILABLE:
        pytest.main([__file__])
    else:
        print("Skipping tests due to missing dependencies")