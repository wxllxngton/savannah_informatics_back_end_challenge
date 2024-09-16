-- Drop the existing database if it exists
DROP DATABASE IF EXISTS savannah_info;

-- Create a new database
CREATE DATABASE savannah_info;

-- Connect to the created database
\c savannah_info;

-- Create the enumerated types
CREATE TYPE order_status_enum AS ENUM ('Incomplete', 'Complete');

-- Create the users table
CREATE TABLE IF NOT EXISTS users (
    UserID serial PRIMARY KEY,
    UserFName text NOT NULL,
    UserLName text NOT NULL,
    UserEmail text UNIQUE NOT NULL
);

-- Create the orders table
CREATE TABLE IF NOT EXISTS orders (
    OrderID serial PRIMARY KEY,
    UserID int NOT NULL,
    OrderItem text NOT NULL,
    OrderAmount numeric(10, 2) NOT NULL,
    OrderStatus order_status_enum NOT NULL,
    OrderTime timestamp DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES users (UserID) ON DELETE CASCADE
);
