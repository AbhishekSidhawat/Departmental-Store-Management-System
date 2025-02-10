-- CREATE THE DATABSE IN MY SQL
create database if not exists super_store;

-- CREATE THE TABLES
create table product(
  product_id int primary key auto_increment,
  name varchar(255) not null,
  category_id int ,
  price decimal(10,2) not null,
  stock_quantity int default 0,
  supplier_id int,
  create_at timestamp default current_timestamp,
  update_at timestamp default current_timestamp on update current_timestamp
);

create table category (
  category_id int primary key auto_increment,
  category_name varchar(255) not nulle
);

create table suppliers(
  supplier_id int primary key auto_increment,
  name varchar(255) not null,
  contact_person varchar (255),
  phone_number varchar(25),
  email varchar(255),
  address text,
  create_at timestamp default current_timestamp,
  update_at timestamp default current_timestamp on update current_timestamp
);


CREATE TABLE sales (
  sale_id INT AUTO_INCREMENT PRIMARY KEY,
  quantity INT NOT NULL,
  sale_price DECIMAL(10, 2) NOT NULL,
  total_price DECIMAL(10, 2) AS (quantity * sale_price) STORED,
  sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  role VARCHAR(50) NOT NULL,   -- Example roles: 'admin', 'manager', 'sales'
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE purchase_orders (
  order_id INT AUTO_INCREMENT PRIMARY KEY,
  quantity INT NOT NULL,
  order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expected_delivery_date TIMESTAMP,
  status VARCHAR(50) DEFAULT 'Pending'   -- Status could be: 'Pending', 'Shipped', 'Delivered'
);

CREATE TABLE inventory_adjustments (
  adjustment_id INT AUTO_INCREMENT PRIMARY KEY,
  adjustment_type VARCHAR(50),    -- E.g., 'Restock', 'Return', 'Damage'
  quantity INT NOT NULL,
  reason TEXT,
  adjusted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE role_permissions (
  permission_id INT AUTO_INCREMENT PRIMARY KEY,
  role VARCHAR(50),         -- E.g., 'admin', 'manager', 'sales_associate'
  permission VARCHAR(255)    -- E.g., 'view_inventory', 'create_sales', 'manage_users'
);

create table customer_details( 
  customer_id int primary key auto_increment,
  name varchar(255) not null,
  phone varchar(25) not null unique,  
  address text not null
);
