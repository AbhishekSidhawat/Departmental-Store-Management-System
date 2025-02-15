-- CREATE THE DATABASE
CREATE DATABASE IF NOT EXISTS super_store;
-- USE THE DATABASE
USE super_store;
-- CREATE THE TABLES
CREATE TABLE category (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(255) NOT NULL
);

CREATE TABLE suppliers (
    supplier_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    contact_person VARCHAR(255),
    phone_number VARCHAR(25),
    email VARCHAR(255),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE product (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    category_id INT,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    supplier_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(category_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,  -- Example roles: 'admin', 'manager', 'sales'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(25) NOT NULL UNIQUE,
    address TEXT NOT NULL
);

CREATE TABLE sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    customer_id INT NOT NULL,
    user_id INT NOT NULL,
    quantity INT NOT NULL,
    sale_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) AS (quantity * sale_price) STORED,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(product_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE purchase_orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    supplier_id INT NOT NULL,
    user_id INT NOT NULL,
    quantity INT NOT NULL,
    total_cost DECIMAL(10,2),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expected_delivery_date TIMESTAMP,
    status VARCHAR(50) DEFAULT 'Pending',  -- Status: 'Pending', 'Shipped', 'Delivered'
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(product_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE inventory_adjustments (
    adjustment_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    adjustment_type VARCHAR(50),    -- E.g., 'Restock', 'Return', 'Damage'
    quantity INT NOT NULL,
    reason TEXT,
    adjusted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);

CREATE TABLE role_permissions (
    permission_id INT AUTO_INCREMENT PRIMARY KEY,
    role VARCHAR(50),         -- E.g., 'admin', 'manager', 'sales_associate'
    permission VARCHAR(255)    -- E.g., 'view_inventory', 'create_sales', 'manage_users'
);

ALTER TABLE customers ADD CONSTRAINT unique_customer_phone UNIQUE (phone);
ALTER TABLE suppliers ADD CONSTRAINT unique_supplier_email UNIQUE (email);
