-- How many customers are there in finsight?
SELECT 
    COUNT(*) AS total_customers
FROM
    customers;

-- Count only "active" customers
SELECT 
    COUNT(*) AS total_customers
FROM
    customers
WHERE
    status = 'active';
    
-- Any customers with blank emails?
SELECT 
    COUNT(*) AS customers_with_empty_emails
FROM
    customers
WHERE
    email IS NULL OR TRIM(email) = '';

-- How many accounts are there of each account type, and what’s the average balance for each type?
SELECT 
    account_type,
    COUNT(*) AS num_accounts,
    AVG(balance) AS avg_balance
FROM
    accounts
GROUP BY account_type
ORDER BY num_accounts DESC;