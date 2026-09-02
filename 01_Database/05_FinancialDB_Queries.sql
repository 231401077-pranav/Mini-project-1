-- ============================================================================
-- SQL Script 5: T-SQL Business Analytical Queries (15 Queries)
-- Database Name: FinancialAnalyticsDB
-- RDBMS Engine: Microsoft SQL Server (T-SQL)
-- Project: Financial Transaction & Customer Analytics System
-- ============================================================================

USE FinancialAnalyticsDB;
GO

-- ----------------------------------------------------------------------------
-- QUERY 1: Executive Key Metrics Summary
-- ----------------------------------------------------------------------------
SELECT 
    COUNT(TransactionID) AS TotalTransactions,
    SUM(TransactionAmount) AS TotalRevenue,
    AVG(TransactionAmount) AS AvgTransactionValue,
    MIN(TransactionAmount) AS MinTransactionValue,
    MAX(TransactionAmount) AS MaxTransactionValue,
    COUNT(DISTINCT CustomerID) AS TotalActiveCustomers,
    SUM(CASE WHEN IsFraud = 1 THEN 1 ELSE 0 END) AS FlaggedFraudTransactions,
    CAST(SUM(CASE WHEN IsFraud = 1 THEN 1.0 ELSE 0 END) * 100.0 / COUNT(TransactionID) AS DECIMAL(5,2)) AS FraudPercentage
FROM dbo.FactTransactions;
GO

-- ----------------------------------------------------------------------------
-- QUERY 2: Top 10 High-Value Customers by Lifetime Spend (Window Function)
-- ----------------------------------------------------------------------------
WITH CustomerSpending AS (
    SELECT 
        c.CustomerID,
        c.FullName,
        c.Gender,
        c.AgeGroup,
        c.City,
        c.State,
        COUNT(f.TransactionID) AS TransactionCount,
        SUM(f.TransactionAmount) AS TotalSpend,
        AVG(f.TransactionAmount) AS AvgSpend,
        DENSE_RANK() OVER (ORDER BY SUM(f.TransactionAmount) DESC) AS SpendRank
    FROM dbo.DimCustomers c
    INNER JOIN dbo.FactTransactions f ON c.CustomerID = f.CustomerID
    GROUP BY c.CustomerID, c.FullName, c.Gender, c.AgeGroup, c.City, c.State
)
SELECT * FROM CustomerSpending
WHERE SpendRank <= 10
ORDER BY SpendRank;
GO

-- ----------------------------------------------------------------------------
-- QUERY 3: Category Revenue & Volume Analysis
-- ----------------------------------------------------------------------------
SELECT 
    cat.SuperCategory,
    cat.CategoryName,
    COUNT(f.TransactionID) AS Volume,
    SUM(f.TransactionAmount) AS TotalRevenue,
    CAST(SUM(f.TransactionAmount) * 100.0 / SUM(SUM(f.TransactionAmount)) OVER() AS DECIMAL(5,2)) AS RevenueSharePct,
    AVG(f.TransactionAmount) AS AvgTransactionValue
FROM dbo.FactTransactions f
INNER JOIN dbo.DimCategories cat ON f.CategoryID = cat.CategoryID
GROUP BY cat.SuperCategory, cat.CategoryName
ORDER BY TotalRevenue DESC;
GO

-- ----------------------------------------------------------------------------
-- QUERY 4: Payment Method Performance & Preference Analysis
-- ----------------------------------------------------------------------------
SELECT 
    pm.PaymentMethodName,
    pm.ChannelType,
    COUNT(f.TransactionID) AS TransactionVolume,
    SUM(f.TransactionAmount) AS TotalRevenue,
    AVG(f.TransactionAmount) AS AvgTransactionValue,
    SUM(CASE WHEN f.IsFraud = 1 THEN 1 ELSE 0 END) AS FraudCount
FROM dbo.FactTransactions f
INNER JOIN dbo.DimPaymentMethods pm ON f.PaymentMethodID = pm.PaymentMethodID
GROUP BY pm.PaymentMethodName, pm.ChannelType
ORDER BY TotalRevenue DESC;
GO

-- ----------------------------------------------------------------------------
-- QUERY 5: Geographic State Performance Ranking
-- ----------------------------------------------------------------------------
SELECT 
    l.State,
    l.Region,
    COUNT(DISTINCT f.CustomerID) AS UniqueCustomers,
    COUNT(f.TransactionID) AS TotalTransactions,
    SUM(f.TransactionAmount) AS TotalRevenue,
    AVG(f.TransactionAmount) AS AvgTransactionValue,
    DENSE_RANK() OVER (ORDER BY SUM(f.TransactionAmount) DESC) AS StateRevenueRank
FROM dbo.FactTransactions f
INNER JOIN dbo.DimLocations l ON f.LocationID = l.LocationID
GROUP BY l.State, l.Region
ORDER BY TotalRevenue DESC;
GO

-- ----------------------------------------------------------------------------
-- QUERY 6: Customer Demographics - Age Group vs Gender Spending Matrix
-- ----------------------------------------------------------------------------
SELECT 
    c.AgeGroup,
    c.Gender,
    COUNT(DISTINCT c.CustomerID) AS CustomerCount,
    COUNT(f.TransactionID) AS TotalTransactions,
    SUM(f.TransactionAmount) AS TotalRevenue,
    AVG(f.TransactionAmount) AS AvgSpendPerTxn
FROM dbo.DimCustomers c
INNER JOIN dbo.FactTransactions f ON c.CustomerID = f.CustomerID
GROUP BY c.AgeGroup, c.Gender
ORDER BY c.AgeGroup, c.Gender;
GO

-- ----------------------------------------------------------------------------
-- QUERY 7: Risk Category Breakdown & Financial Exposure
-- ----------------------------------------------------------------------------
SELECT 
    RiskCategory,
    COUNT(TransactionID) AS TransactionCount,
    SUM(TransactionAmount) AS TotalAmount,
    AVG(TransactionAmount) AS AvgAmount,
    CAST(COUNT(TransactionID) * 100.0 / SUM(COUNT(TransactionID)) OVER() AS DECIMAL(5,2)) AS ExposurePct
FROM dbo.FactTransactions
GROUP BY RiskCategory
ORDER BY TotalAmount DESC;
GO

-- ----------------------------------------------------------------------------
-- QUERY 8: Hourly Transaction Volume & Peak Spending Heatmap Query
-- ----------------------------------------------------------------------------
SELECT 
    d.Hour,
    d.IsWeekend,
    COUNT(f.TransactionID) AS TransactionVolume,
    SUM(f.TransactionAmount) AS TotalRevenue,
    AVG(f.TransactionAmount) AS AvgTransactionValue
FROM dbo.FactTransactions f
INNER JOIN dbo.DimDates d ON f.DateKey = d.DateKey AND f.Hour = d.Hour
GROUP BY d.Hour, d.IsWeekend
ORDER BY d.Hour, d.IsWeekend;
GO

-- ----------------------------------------------------------------------------
-- QUERY 9: Top 10 Merchants by Total Sales Volume
-- ----------------------------------------------------------------------------
SELECT TOP 10
    MerchantName,
    COUNT(TransactionID) AS TotalTransactions,
    SUM(TransactionAmount) AS TotalMerchantSales,
    AVG(TransactionAmount) AS AvgTicketSize
FROM dbo.FactTransactions
GROUP BY MerchantName
ORDER BY TotalMerchantSales DESC;
GO

-- ----------------------------------------------------------------------------
-- QUERY 10: Fraud Detection Deep-Dive by Spending Category
-- ----------------------------------------------------------------------------
SELECT 
    cat.CategoryName,
    COUNT(f.TransactionID) AS TotalTxns,
    SUM(CASE WHEN f.IsFraud = 1 THEN 1 ELSE 0 END) AS FraudTxns,
    SUM(CASE WHEN f.IsFraud = 1 THEN f.TransactionAmount ELSE 0 END) AS FraudAmount,
    CAST(SUM(CASE WHEN f.IsFraud = 1 THEN 1.0 ELSE 0 END) * 100.0 / COUNT(f.TransactionID) AS DECIMAL(5,2)) AS CategoryFraudRate
FROM dbo.FactTransactions f
INNER JOIN dbo.DimCategories cat ON f.CategoryID = cat.CategoryID
GROUP BY cat.CategoryName
HAVING SUM(CASE WHEN f.IsFraud = 1 THEN 1 ELSE 0 END) > 0
ORDER BY FraudTxns DESC;
GO

-- ----------------------------------------------------------------------------
-- QUERY 11: Customer RFM Segmentation Base Query (Recency, Frequency, Monetary)
-- ----------------------------------------------------------------------------
WITH CustomerRFM AS (
    SELECT 
        CustomerID,
        COUNT(TransactionID) AS Frequency,
        SUM(TransactionAmount) AS Monetary,
        MAX(TransactionTimestamp) AS LastTransactionDate
    FROM dbo.FactTransactions
    GROUP BY CustomerID
)
SELECT 
    CustomerID,
    Frequency,
    Monetary,
    LastTransactionDate,
    NTILE(4) OVER (ORDER BY Frequency DESC) AS FrequencyScore,
    NTILE(4) OVER (ORDER BY Monetary DESC) AS MonetaryScore
FROM CustomerRFM
ORDER BY Monetary DESC;
GO

-- ----------------------------------------------------------------------------
-- QUERY 12: High-Risk Outlier Transactions (> 3 Standard Deviations)
-- ----------------------------------------------------------------------------
WITH Stats AS (
    SELECT 
        AVG(TransactionAmount) AS MeanAmt,
        STDEV(TransactionAmount) AS StdDevAmt
    FROM dbo.FactTransactions
)
SELECT 
    f.TransactionNum,
    f.TransactionTimestamp,
    c.FullName,
    f.MerchantName,
    f.TransactionAmount,
    s.MeanAmt,
    s.StdDevAmt,
    (f.TransactionAmount - s.MeanAmt) / s.StdDevAmt AS ZScore
FROM dbo.FactTransactions f
CROSS JOIN Stats s
INNER JOIN dbo.DimCustomers c ON f.CustomerID = c.CustomerID
WHERE (f.TransactionAmount - s.MeanAmt) / s.StdDevAmt > 3.0
ORDER BY f.TransactionAmount DESC;
GO

-- ----------------------------------------------------------------------------
-- QUERY 13: Cumulative Revenue Trend by Day (Window Running Total)
-- ----------------------------------------------------------------------------
SELECT 
    d.TransactionDate,
    COUNT(f.TransactionID) AS DailyTxnVolume,
    SUM(f.TransactionAmount) AS DailyRevenue,
    SUM(SUM(f.TransactionAmount)) OVER (ORDER BY d.TransactionDate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS CumulativeRevenue
FROM dbo.FactTransactions f
INNER JOIN dbo.DimDates d ON f.DateKey = d.DateKey AND f.Hour = d.Hour
GROUP BY d.TransactionDate
ORDER BY d.TransactionDate;
GO

-- ----------------------------------------------------------------------------
-- QUERY 14: Cross-Tabulation of Super Category vs Region Revenue
-- ----------------------------------------------------------------------------
SELECT 
    cat.SuperCategory,
    SUM(CASE WHEN l.Region = 'Northeast' THEN f.TransactionAmount ELSE 0 END) AS Northeast_Revenue,
    SUM(CASE WHEN l.Region = 'Midwest' THEN f.TransactionAmount ELSE 0 END) AS Midwest_Revenue,
    SUM(CASE WHEN l.Region = 'South' THEN f.TransactionAmount ELSE 0 END) AS South_Revenue,
    SUM(CASE WHEN l.Region = 'West' THEN f.TransactionAmount ELSE 0 END) AS West_Revenue,
    SUM(f.TransactionAmount) AS Total_Revenue
FROM dbo.FactTransactions f
INNER JOIN dbo.DimCategories cat ON f.CategoryID = cat.CategoryID
INNER JOIN dbo.DimLocations l ON f.LocationID = l.LocationID
GROUP BY cat.SuperCategory
ORDER BY Total_Revenue DESC;
GO

-- ----------------------------------------------------------------------------
-- QUERY 15: Regional Fraud Concentration Index
-- ----------------------------------------------------------------------------
SELECT 
    l.Region,
    COUNT(f.TransactionID) AS TotalTxns,
    SUM(CASE WHEN f.IsFraud = 1 THEN 1 ELSE 0 END) AS FraudCount,
    SUM(f.TransactionAmount) AS TotalVolume,
    SUM(CASE WHEN f.IsFraud = 1 THEN f.TransactionAmount ELSE 0 END) AS FraudVolume,
    CAST(SUM(CASE WHEN f.IsFraud = 1 THEN 1.0 ELSE 0 END) * 100.0 / COUNT(f.TransactionID) AS DECIMAL(5,2)) AS RegionalFraudPct
FROM dbo.FactTransactions f
INNER JOIN dbo.DimLocations l ON f.LocationID = l.LocationID
GROUP BY l.Region
ORDER BY RegionalFraudPct DESC;
GO

PRINT 'All 15 T-SQL Analytical Queries executed successfully.';
GO
