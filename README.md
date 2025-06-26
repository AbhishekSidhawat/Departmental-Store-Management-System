# Departmental Store Management System

A role-based departmental store management system built using **Flask**, **MySQL**, and **SQLAlchemy**. This system streamlines operations like product management, inventory tracking, sales handling, customer records, and performance reporting for daily, weekly, and monthly analysis.

## Features

- **Role-Based Access Control**
  - **Manager**: Full access to all modules
  - **Cashier**: Restricted to sales and inventory view

- **User Authentication**
  - Secure login and registration using hashed passwords (Bcrypt)

- **Product Management**
  - Add new products or update stock of existing ones
  - Set low stock alert threshold

- **Sales Management**
  - Record multi-product sales under a single customer entry
  - Auto-check and update stock
  - Dynamic bill generation after sale

- **Customer Management**
  - Avoid duplicate entries based on phone number
  - Store and reuse customer details

- **Inventory Tracking**
  - Monitor all product stock levels
  - Highlight low stock items

- **Sales & Inventory Analysis**
  - View total sales for daily, weekly, and monthly periods
  - Track overall stock value
  - Identify low-stock items for restocking

- **Sales History**
  - Filter and search sales by customer name or phone number

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Frontend**: HTML, Jinja, Bootstrap (optional)
- **Database**: MySQL (using PyMySQL driver)
- **Security**: Bcrypt for password hashing
- **Deployment**: Localhost (for development)
