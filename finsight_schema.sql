-- Creating the database
CREATE DATABASE finsight;

-- Selecting the database
USE finsight;

-- Creating customers table
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_type ENUM('individual', 'business') NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    business_name VARCHAR(100),
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(100),
    date_of_birth DATE,
    registration_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status ENUM('active', 'suspended', 'closed') NOT NULL DEFAULT 'active',
    address VARCHAR(500),
    country VARCHAR(100)
);

-- Creating accounts table
CREATE TABLE accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    account_type ENUM('checking', 'savings', 'investment', 'loan') NOT NULL,
    currency_code CHAR(3) NOT NULL,
    balance DECIMAL NOT NULL DEFAULT 0.00,
    opened_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status ENUM('active', 'closed', 'frozen') NOT NULL DEFAULT 'active',
    FOREIGN KEY (customer_id)
        REFERENCES customers (customer_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- Creating currencies table
CREATE TABLE currencies (
    currencty_code CHAR(3) PRIMARY KEY,
    currency_name	VARCHAR(50) NOT NULL,
    symbol	VARCHAR(5),
    exchange_rate	DECIMAL (15,6) NOT NULL DEFAULT 1.00
);

-- Change any mispelled column name
ALTER TABLE currencies CHANGE currencty_code currency_code	CHAR(3) NOT NULL;

-- Inserting sample currencies into currencies table
INSERT INTO currencies (currency_code, currency_name, symbol, exchange_rate) VALUES
('USD', 'United States Dollar', '$', 1.000000),
('EUR', 'Euro', '€', 0.920000),
('GBP', 'British Pound', '£', 0.810000),
('INR', 'Indian Rupee', '₹', 79.500000);

-- Check the built of any table
DESCRIBE currencies;

-- Building the transactions table
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    type ENUM('deposit', 'withdrawal', 'transfer', 'payment', 'exchange') NOT NULL,
    amount DECIMAL(15 , 2 ) NOT NULL,
    currency_code CHAR(3) NOT NULL,
    related_account_id INT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(255),
    FOREIGN KEY (account_id)
        REFERENCES accounts (account_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (currency_code)
        REFERENCES currencies (currency_code),
    FOREIGN KEY (related_account_id)
        REFERENCES accounts (account_id)
        ON UPDATE CASCADE ON DELETE SET NULL
);