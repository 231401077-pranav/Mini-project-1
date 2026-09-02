-- ============================================================================
-- SQL Script 3: Financial Analytics Bulk Data Load & Verification
-- Database Name: FinancialAnalyticsDB
-- RDBMS Engine: Microsoft SQL Server (T-SQL)
-- Project: Financial Transaction & Customer Analytics System
-- ============================================================================

USE FinancialAnalyticsDB;
GO

PRINT 'Loading dimension and fact data into FinancialAnalyticsDB...';
GO

-- 1. Load DimCategories
BULK INSERT dbo.DimCategories
FROM '/Users/pranav/Downloads/Financial_Analytics/02_Program/data/dim_categories.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);
GO

-- 2. Load DimPaymentMethods
BULK INSERT dbo.DimPaymentMethods
FROM '/Users/pranav/Downloads/Financial_Analytics/02_Program/data/dim_payment_methods.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);
GO

-- 3. Load DimCustomers
BULK INSERT dbo.DimCustomers
FROM '/Users/pranav/Downloads/Financial_Analytics/02_Program/data/dim_customers.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);
GO

-- 4. Load DimLocations
BULK INSERT dbo.DimLocations
FROM '/Users/pranav/Downloads/Financial_Analytics/02_Program/data/dim_locations.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);
GO

-- 5. Load DimDates
BULK INSERT dbo.DimDates
FROM '/Users/pranav/Downloads/Financial_Analytics/02_Program/data/dim_dates.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);
GO

-- 6. Load FactTransactions
BULK INSERT dbo.FactTransactions
FROM '/Users/pranav/Downloads/Financial_Analytics/02_Program/data/fact_transactions.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);
GO

-- Row Count Verification
SELECT 'DimCustomers' AS TableName, COUNT(*) AS RecordCount FROM dbo.DimCustomers
UNION ALL
SELECT 'DimCategories', COUNT(*) FROM dbo.DimCategories
UNION ALL
SELECT 'DimPaymentMethods', COUNT(*) FROM dbo.DimPaymentMethods
UNION ALL
SELECT 'DimLocations', COUNT(*) FROM dbo.DimLocations
UNION ALL
SELECT 'DimDates', COUNT(*) FROM dbo.DimDates
UNION ALL
SELECT 'FactTransactions', COUNT(*) FROM dbo.FactTransactions;
GO

PRINT 'Data loading into FinancialAnalyticsDB completed successfully.';
GO
