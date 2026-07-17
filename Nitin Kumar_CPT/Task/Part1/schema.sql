-- Part A - SQL Exercise
-- Schema and sample data setup for products_yesterday and products_today
-- Run this first to create and populate both tables before running the task queries.

CREATE TABLE products_yesterday (
    product_id   INT PRIMARY KEY,
    product_name VARCHAR(100),
    price        DECIMAL(10,2),
    status       VARCHAR(20)
);

CREATE TABLE products_today (
    product_id   INT PRIMARY KEY,
    product_name VARCHAR(100),
    price        DECIMAL(10,2),
    status       VARCHAR(20)
);

INSERT INTO products_yesterday (product_id, product_name, price, status) VALUES
(1001, 'Coffee Mug',     12.50, 'ACTIVE'),
(1002, 'Laptop Stand',   38.00, 'ACTIVE'),
(1003, 'Wireless Mouse', 19.99, 'ACTIVE'),
(1004, 'Old Keyboard',   29.99, 'DISCONTINUED'),
(1005, 'Notebook',       4.50,  'ACTIVE'),
(1008, 'Desk Lamp',      24.00, 'ACTIVE');

INSERT INTO products_today (product_id, product_name, price, status) VALUES
(1001, 'Coffee Mug',     12.50, 'ACTIVE'),
(1002, 'Laptop Stand',   35.00, 'ACTIVE'),
(1003, 'Wireless Mouse', 21.99, 'ACTIVE'),
(1005, 'Notebook',       4.50,  'INACTIVE'),
(1006, 'Webcam',         59.00, 'ACTIVE'),
(1007, 'USB Cable',      7.99,  'ACTIVE'),
(1008, 'Desk Lamp',      24.00, 'ACTIVE');
