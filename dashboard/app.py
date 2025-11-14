#!/usr/bin/env python3
"""
Streamlit dashboard for e-commerce data visualization
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Database path
DB_PATH = "../database/ecom.db"

# Helper function to get database connection
def get_db_connection():
    if not os.path.exists(DB_PATH):
        st.error("Database not found. Please run the data pipeline first.")
        st.stop()
    conn = sqlite3.connect(DB_PATH)
    return conn

# Page configuration
st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 E-commerce Analytics Dashboard")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.selectbox(
    "Choose a page",
    ["Overview", "Customers", "Products", "Orders", "Analytics"]
)

# Overview page
if page == "Overview":
    st.header("System Overview")
    
    try:
        conn = get_db_connection()
        
        # Get row counts for each table
        tables = ['customers', 'products', 'orders', 'order_items', 'payments']
        row_counts = {}
        
        for table in tables:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            row_counts[table] = count
        
        conn.close()
        
        # Display metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Customers", f"{row_counts['customers']:,}")
        col2.metric("Products", f"{row_counts['products']:,}")
        col3.metric("Orders", f"{row_counts['orders']:,}")
        col4.metric("Order Items", f"{row_counts['order_items']:,}")
        col5.metric("Payments", f"{row_counts['payments']:,}")
        
        # Show recent orders
        st.subheader("Recent Orders")
        conn = get_db_connection()
        recent_orders = pd.read_sql_query("""
            SELECT order_id, customer_id, order_date, total_amount
            FROM orders
            ORDER BY order_date DESC
            LIMIT 10
        """, conn)
        conn.close()
        
        st.dataframe(recent_orders)
        
    except Exception as e:
        st.error(f"Error loading overview data: {str(e)}")

# Customers page
elif page == "Customers":
    st.header("Customers")
    
    try:
        conn = get_db_connection()
        customers_df = pd.read_sql_query("""
            SELECT * FROM customers
            ORDER BY signup_date DESC
            LIMIT 100
        """, conn)
        conn.close()
        
        st.subheader("Customer List")
        st.dataframe(customers_df)
        
        # Signup trend
        st.subheader("Signup Trend")
        customers_df['signup_date'] = pd.to_datetime(customers_df['signup_date'])
        signup_trend = customers_df.groupby(customers_df['signup_date'].dt.date).size().reset_index().rename(columns={0: 'count'})
        
        fig = px.line(signup_trend, x='signup_date', y='count', title='Customer Signups Over Time')
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading customer data: {str(e)}")

# Products page
elif page == "Products":
    st.header("Products")
    
    try:
        conn = get_db_connection()
        products_df = pd.read_sql_query("""
            SELECT * FROM products
        """, conn)
        conn.close()
        
        st.subheader("Product List")
        st.dataframe(products_df)
        
        # Category distribution
        st.subheader("Products by Category")
        category_counts = products_df['category'].value_counts().reset_index().rename(columns={'index': 'category', 0: 'count'})
        
        fig = px.bar(category_counts, x='category', y='count', title='Products by Category')
        st.plotly_chart(fig, use_container_width=True)
        
        # Price distribution
        st.subheader("Price Distribution")
        fig = px.histogram(products_df, x='price', nbins=30, title='Product Price Distribution')
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading product data: {str(e)}")

# Orders page
elif page == "Orders":
    st.header("Orders")
    
    try:
        conn = get_db_connection()
        orders_df = pd.read_sql_query("""
            SELECT * FROM orders
            ORDER BY order_date DESC
            LIMIT 100
        """, conn)
        conn.close()
        
        st.subheader("Order List")
        st.dataframe(orders_df)
        
        # Order trend
        st.subheader("Order Trend")
        orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
        order_trend = orders_df.groupby(orders_df['order_date'].dt.date).size().reset_index().rename(columns={0: 'count'})
        
        fig = px.line(order_trend, x='order_date', y='count', title='Orders Over Time')
        st.plotly_chart(fig, use_container_width=True)
        
        # Order value distribution
        st.subheader("Order Value Distribution")
        fig = px.histogram(orders_df, x='total_amount', nbins=30, title='Order Value Distribution')
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error loading order data: {str(e)}")

# Analytics page
elif page == "Analytics":
    st.header("Analytics")
    
    try:
        conn = get_db_connection()
        
        # Top customers by spend
        st.subheader("Top Customers by Spend")
        top_customers = pd.read_sql_query("""
            SELECT 
                c.first_name || ' ' || c.last_name as customer_name,
                COUNT(o.order_id) as order_count,
                SUM(o.total_amount) as total_spend
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.first_name, c.last_name
            ORDER BY total_spend DESC
            LIMIT 10
        """, conn)
        
        fig = px.bar(top_customers, x='customer_name', y='total_spend', title='Top 10 Customers by Spend')
        st.plotly_chart(fig, use_container_width=True)
        
        # Revenue by category
        st.subheader("Revenue by Category")
        category_revenue = pd.read_sql_query("""
            SELECT 
                p.category,
                SUM(oi.line_total) as revenue
            FROM products p
            JOIN order_items oi ON p.product_id = oi.product_id
            GROUP BY p.category
            ORDER BY revenue DESC
        """, conn)
        
        fig = px.pie(category_revenue, values='revenue', names='category', title='Revenue by Category')
        st.plotly_chart(fig, use_container_width=True)
        
        # Daily revenue trend
        st.subheader("Daily Revenue Trend")
        daily_revenue = pd.read_sql_query("""
            SELECT 
                DATE(order_date) as date,
                SUM(total_amount) as revenue
            FROM orders
            GROUP BY DATE(order_date)
            ORDER BY date
        """, conn)
        
        fig = px.line(daily_revenue, x='date', y='revenue', title='Daily Revenue Trend')
        st.plotly_chart(fig, use_container_width=True)
        
        conn.close()
        
    except Exception as e:
        st.error(f"Error loading analytics data: {str(e)}")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("E-commerce Analytics Dashboard v1.0")