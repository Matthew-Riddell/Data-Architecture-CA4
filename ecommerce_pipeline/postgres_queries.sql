-- Matthew Riddell D00245674
-- PostgreSQL Queries

-- 1. select all stores
SELECT * FROM stores;

-- 2. select the first 5 products
SELECT * FROM products LIMIT 5;

-- 3. count products per store

SELECT
    s.name,
    COUNT(*) AS product_count
FROM products p
JOIN stores s
ON p.store_id = s.id
GROUP BY s.name;

-- 4. average product price per store

SELECT
    s.name,
    AVG(p.price) AS average_price
FROM products p
JOIN stores s
ON p.store_id = s.id
GROUP BY s.name;

