-- SQL Analytics Queries for E-commerce Data Analysis

-- 1. Top 50 customers by total spend
-- This query identifies the highest spending customers based on their order history
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_spend
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.email
ORDER BY total_spend DESC
LIMIT 50;

-- 2. Top products by revenue
-- This query identifies the highest revenue generating products
SELECT 
    p.product_id,
    p.name AS product_name,
    p.category,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.line_total) AS total_revenue
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.name, p.category
ORDER BY total_revenue DESC
LIMIT 50;

-- 3. Revenue by category
-- This query shows revenue distribution across product categories
SELECT 
    p.category,
    COUNT(DISTINCT p.product_id) AS product_count,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.line_total) AS total_revenue,
    AVG(oi.line_total) AS avg_revenue_per_item
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- 4. Revenue time series (daily)
-- This query shows daily revenue trends
SELECT 
    DATE(o.order_date) AS order_day,
    COUNT(DISTINCT o.order_id) AS daily_orders,
    SUM(o.total_amount) AS daily_revenue
FROM orders o
GROUP BY DATE(o.order_date)
ORDER BY order_day;

-- 5. Revenue time series (weekly)
-- This query shows weekly revenue trends
SELECT 
    strftime('%Y-%W', o.order_date) AS order_week,
    COUNT(DISTINCT o.order_id) AS weekly_orders,
    SUM(o.total_amount) AS weekly_revenue
FROM orders o
GROUP BY strftime('%Y-%W', o.order_date)
ORDER BY order_week;

-- 6. Revenue time series (monthly)
-- This query shows monthly revenue trends
SELECT 
    strftime('%Y-%m', o.order_date) AS order_month,
    COUNT(DISTINCT o.order_id) AS monthly_orders,
    SUM(o.total_amount) AS monthly_revenue
FROM orders o
GROUP BY strftime('%Y-%m', o.order_date)
ORDER BY order_month;

-- 7. Average order value per customer
-- This query calculates the average order value for each customer
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_spend,
    AVG(o.total_amount) AS avg_order_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(o.order_id) > 0
ORDER BY avg_order_value DESC
LIMIT 50;

-- 8. Fraud-like anomalies (orders with mismatched payments)
-- This query identifies potential anomalies where payment amounts don't match order totals
SELECT 
    o.order_id,
    o.total_amount AS order_total,
    p.amount AS payment_amount,
    ABS(o.total_amount - p.amount) AS discrepancy
FROM orders o
JOIN payments p ON o.order_id = p.order_id
WHERE ABS(o.total_amount - p.amount) > 0.01
ORDER BY discrepancy DESC;

-- 9. Power user analysis (customers with > 90th percentile order volume)
-- This query identifies power users based on order volume
WITH customer_order_counts AS (
    SELECT 
        c.customer_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        COUNT(o.order_id) AS order_count
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name
),
percentile_90 AS (
    SELECT order_count AS p90_threshold
    FROM customer_order_counts
    ORDER BY order_count
    LIMIT 1 OFFSET (SELECT CAST(COUNT(*) * 0.9 AS INTEGER) FROM customer_order_counts)
)
SELECT 
    coc.customer_id,
    coc.customer_name,
    coc.order_count
FROM customer_order_counts coc
CROSS JOIN percentile_90 p90
WHERE coc.order_count > p90.p90_threshold
ORDER BY coc.order_count DESC;