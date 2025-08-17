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
    a.account_type,
    AVG(totals.total_balance) AS avg_balance_calculated
FROM
    accounts AS a
        JOIN
    (SELECT 
        account_id, SUM(amount) AS total_balance
    FROM
        transactions
    GROUP BY account_id) totals ON a.account_id = totals.account_id
GROUP BY a.account_type
ORDER BY avg_balance_calculated DESC;