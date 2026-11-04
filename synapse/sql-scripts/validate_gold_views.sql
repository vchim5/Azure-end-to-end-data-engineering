USE gold_db;
GO

-- Verify the Customer view
SELECT COUNT(*) AS TotalCustomers
FROM dbo.Customer;

-- Validate end-to-end test records
SELECT customer_id, first_name, last_name
FROM dbo.Customer
WHERE last_name IN (
    'PipelineTest01',
    'PipelineTest02'
);

-- Check available Gold views
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.VIEWS
WHERE TABLE_SCHEMA = 'dbo'
ORDER BY TABLE_NAME;
