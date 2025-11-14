#!/usr/bin/env python3
"""
FastAPI REST API for e-commerce data access
"""

import sqlite3
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
import os
from datetime import datetime

# Create FastAPI app
app = FastAPI(
    title="E-commerce Data API",
    description="REST API for accessing e-commerce synthetic data",
    version="1.0.0"
)

# Database path
DB_PATH = "../database/ecom.db"

# Pydantic models for response data
class Customer(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    email: str
    signup_date: str

class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float

class Order(BaseModel):
    order_id: int
    customer_id: int
    order_date: str
    total_amount: float

class OrderItem(BaseModel):
    order_item_id: int
    order_id: int
    product_id: int
    quantity: int
    line_total: float

class Payment(BaseModel):
    payment_id: int
    order_id: int
    payment_method: str
    amount: float
    payment_date: str

# Helper function to get database connection
def get_db_connection():
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=500, detail="Database not found")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "E-commerce Data API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Customers endpoints
@app.get("/customers/", response_model=List[Customer])
async def get_customers(
    skip: int = 0, 
    limit: int = Query(100, le=1000),
    name: Optional[str] = None
):
    """Get customers with optional name filtering"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if name:
            cursor.execute("""
                SELECT * FROM customers 
                WHERE first_name LIKE ? OR last_name LIKE ?
                LIMIT ? OFFSET ?
            """, (f"%{name}%", f"%{name}%", limit, skip))
        else:
            cursor.execute("""
                SELECT * FROM customers 
                LIMIT ? OFFSET ?
            """, (limit, skip))
        
        customers = cursor.fetchall()
        conn.close()
        
        return [dict(customer) for customer in customers]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int):
    """Get a specific customer by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE customer_id = ?", (customer_id,))
        customer = cursor.fetchone()
        conn.close()
        
        if customer is None:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        return dict(customer)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Products endpoints
@app.get("/products/", response_model=List[Product])
async def get_products(
    skip: int = 0, 
    limit: int = Query(100, le=1000),
    category: Optional[str] = None
):
    """Get products with optional category filtering"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if category:
            cursor.execute("""
                SELECT * FROM products 
                WHERE category = ?
                LIMIT ? OFFSET ?
            """, (category, limit, skip))
        else:
            cursor.execute("""
                SELECT * FROM products 
                LIMIT ? OFFSET ?
            """, (limit, skip))
        
        products = cursor.fetchall()
        conn.close()
        
        return [dict(product) for product in products]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    """Get a specific product by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
        product = cursor.fetchone()
        conn.close()
        
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return dict(product)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Orders endpoints
@app.get("/orders/", response_model=List[Order])
async def get_orders(
    skip: int = 0, 
    limit: int = Query(100, le=1000),
    customer_id: Optional[int] = None
):
    """Get orders with optional customer filtering"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if customer_id:
            cursor.execute("""
                SELECT * FROM orders 
                WHERE customer_id = ?
                LIMIT ? OFFSET ?
            """, (customer_id, limit, skip))
        else:
            cursor.execute("""
                SELECT * FROM orders 
                LIMIT ? OFFSET ?
            """, (limit, skip))
        
        orders = cursor.fetchall()
        conn.close()
        
        return [dict(order) for order in orders]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int):
    """Get a specific order by ID"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
        order = cursor.fetchone()
        conn.close()
        
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return dict(order)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Analytics endpoints
@app.get("/analytics/revenue/daily")
async def get_daily_revenue():
    """Get daily revenue summary"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                DATE(order_date) as date,
                COUNT(*) as order_count,
                SUM(total_amount) as revenue
            FROM orders
            GROUP BY DATE(order_date)
            ORDER BY date
        """)
        results = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/top-customers")
async def get_top_customers(limit: int = Query(10, le=100)):
    """Get top customers by total spend"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                c.customer_id,
                c.first_name,
                c.last_name,
                COUNT(o.order_id) as order_count,
                SUM(o.total_amount) as total_spend
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.first_name, c.last_name
            ORDER BY total_spend DESC
            LIMIT ?
        """, (limit,))
        results = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/top-products")
async def get_top_products(limit: int = Query(10, le=100)):
    """Get top products by revenue"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                p.product_id,
                p.name,
                p.category,
                SUM(oi.quantity) as total_quantity,
                SUM(oi.line_total) as total_revenue
            FROM products p
            JOIN order_items oi ON p.product_id = oi.product_id
            GROUP BY p.product_id, p.name, p.category
            ORDER BY total_revenue DESC
            LIMIT ?
        """, (limit,))
        results = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)