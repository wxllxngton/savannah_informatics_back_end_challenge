-- Drop the existing database if it exists
DROP DATABASE IF EXISTS savannah_info;

-- Create a new database
CREATE DATABASE savannah_info;

-- Connect to the created database
\c savannah_info;

-- Create the enumerated types
CREATE TYPE order_status_enum AS ENUM ('Incomplete', 'Complete');

-- Create the customers table
CREATE TABLE IF NOT EXISTS customers (
    CustomerID serial PRIMARY KEY,
    CustomerFName text NOT NULL,
    CustomerLName text NOT NULL,
    CustomerPhoneNo numeric(12) NOT NULL
);

-- Create the orders table
CREATE TABLE IF NOT EXISTS orders (
    OrderID serial PRIMARY KEY,
    CustomerID int NOT NULL,
    OrderItem text NOT NULL,
    OrderAmount numeric(10) NOT NULL,
    OrderStatus order_status_enum NOT NULL,
    OrderTime timestamp DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CustomerID) REFERENCES customers (CustomerID) ON DELETE CASCADE
);

