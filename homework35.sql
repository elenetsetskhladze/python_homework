CREATE DATABASE shop_db;

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE customer_profiles (
    profile_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL UNIQUE REFERENCES customers(customer_id) ON DELETE CASCADE,
    phone_number VARCHAR(30),
    address VARCHAR(255)
);

CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact_email VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    supplier_id INT NOT NULL REFERENCES suppliers(supplier_id)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id INT NOT NULL REFERENCES customers(customer_id)
);

CREATE TABLE order_products (
    order_product_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES products(product_id),
    quantity INT NOT NULL CHECK (quantity > 0)
);
