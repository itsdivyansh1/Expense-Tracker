-- -- Create the database (if it doesn't exist)
-- CREATE DATABASE IF NOT EXISTS expense_tracker;

-- -- Use the expense_tracker database
-- USE expense_tracker;

-- Create the table for daily expenses
CREATE TABLE daily_expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    category VARCHAR(255) NOT NULL,
    expense DECIMAL(10, 2) NOT NULL
);

-- Create the table for monthly expenses
CREATE TABLE monthly_expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(255) NOT NULL,
    expense DECIMAL(10, 2) NOT NULL
);

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL
);