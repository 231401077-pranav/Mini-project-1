-- ============================================================================
-- SQL Script 4: Analytical SQL Views
-- Database Name: FinancialAnalyticsDB
-- RDBMS Engine: Microsoft SQL Server (T-SQL)
-- Project: Financial Transaction & Customer Analytics System
-- ============================================================================

USE FinancialAnalyticsDB;
GO

-- 1. Executive Financial Overview View
IF OBJECT_ID('dbo.vw_ExecutiveOverview', 'V') IS NOT NULL DROP VIEW dbo.vw_ExecutiveOverview;
GO
CREATE VIEW dbo.vw_ExecutiveOverview AS
SELECT 
    d.Year,
    d.Quarter,
    d.Month,
    d.MonthName,
    COUNT(f.TransactionID) AS TotalTransactions,
    SUM(f.TransactionAmount) AS TotalRevenue,
    AVG(f.TransactionAmount) AS AvgTransactionValue,
    COUNT(DISTINCT f.CustomerID) AS ActiveCustomers,
    SUM(CASE WHEN f.IsFraud = 1 THEN 1 ELSE 0 END) AS TotalFraudTransactions,
    SUM(CASE WHEN f.IsFraud = 1 THEN f.TransactionAmount ELSE 0 END) AS TotalFraudAmount
FROM dbo.FactTransactions f
INNER JOIN dbo.DimDates d ON f.DateKey = d.DateKey AND f.Hour = d.Hour
GROUP BY d.Year, d.Quarter, d.Month, d.MonthName;
GO

-- 2. Customer Spending Analytics View
IF OBJECT_ID('dbo.vw_CustomerAnalytics', 'V') IS NOT NULL DROP VIEW dbo.vw_CustomerAnalytics;
GO
CREATE VIEW dbo.vw_CustomerAnalytics AS
SELECT 
    c.CustomerID,
    c.FullName,
    c.Gender,
    c.Age,
    c.AgeGroup,
    c.JobTitle,
    c.City,
    c.State,
    COUNT(f.TransactionID) AS TotalTransactions,
    SUM(f.TransactionAmount) AS LifetimeSpend,
    AVG(f.TransactionAmount) AS AvgSpendPerTxn,
    MAX(f.TransactionAmount) AS MaxSingleSpend,
    SUM(CASE WHEN f.IsFraud = 1 THEN 1 ELSE 0 END) AS FraudCount,
    DENSE_RANK() OVER (ORDER BY SUM(f.TransactionAmount) DESC) AS CustomerRank
FROM dbo.DimCustomers c
INNER JOIN dbo.FactTransactions f ON c.CustomerID = f.CustomerID
GROUP BY c.CustomerID, c.FullName, c.Gender, c.Age, c.AgeGroup, c.JobTitle, c.City, c.State;
GO

-- 3. Category & Payment Method Performance View
IF OBJECT_ID('dbo.vw_CategoryPerformance', 'V') IS NOT NULL DROP VIEW dbo.vw_CategoryPerformance;
GO
CREATE VIEW dbo.vw_CategoryPerformance AS
SELECT 
    cat.SuperCategory,
    cat.CategoryName,
    pm.PaymentMethodName,
    pm.ChannelType,
    COUNT(f.TransactionID) AS TransactionVolume,
    SUM(f.TransactionAmount) AS TotalRevenue,
    AVG(f.TransactionAmount) AS AvgTransactionValue,
    MIN(f.TransactionAmount) AS MinAmount,
    MAX(f.TransactionAmount) AS MaxAmount
FROM dbo.FactTransactions f
INNER JOIN dbo.DimCategories cat ON f.CategoryID = cat.CategoryID
INNER JOIN dbo.DimPaymentMethods pm ON f.PaymentMethodID = pm.PaymentMethodID
GROUP BY cat.SuperCategory, cat.CategoryName, pm.PaymentMethodName, pm.ChannelType;
GO

-- 4. Geographic Financial Distribution View
IF OBJECT_ID('dbo.vw_GeographicDistribution', 'V') IS NOT NULL DROP VIEW dbo.vw_GeographicDistribution;
GO
CREATE VIEW dbo.vw_GeographicDistribution AS
SELECT 
    l.Region,
    l.State,
    l.City,
    COUNT(DISTINCT f.CustomerID) AS CustomerCount,
    COUNT(f.TransactionID) AS TotalTransactions,
    SUM(f.TransactionAmount) AS TotalRevenue,
    AVG(f.TransactionAmount) AS AvgTransactionValue,
    SUM(CASE WHEN f.IsFraud = 1 THEN 1 ELSE 0 END) AS FraudCount
FROM dbo.FactTransactions f
INNER JOIN dbo.DimLocations l ON f.LocationID = l.LocationID
GROUP BY l.Region, l.State, l.City;
GO

-- 5. Risk & Fraud Anomaly View
IF OBJECT_ID('dbo.vw_RiskAndFraudAnalytics', 'V') IS NOT NULL DROP VIEW dbo.vw_RiskAndFraudAnalytics;
GO
CREATE VIEW dbo.vw_RiskAndFraudAnalytics AS
SELECT 
    f.TransactionID,
    f.TransactionNum,
    f.TransactionTimestamp,
    c.FullName AS CustomerName,
    c.CardNumber,
    c.City,
    c.State,
    cat.CategoryName,
    f.MerchantName,
    pm.PaymentMethodName,
    f.TransactionAmount,
    f.IsFraud,
    f.RiskCategory
FROM dbo.FactTransactions f
INNER JOIN dbo.DimCustomers c ON f.CustomerID = c.CustomerID
INNER JOIN dbo.DimCategories cat ON f.CategoryID = cat.CategoryID
INNER JOIN dbo.DimPaymentMethods pm ON f.PaymentMethodID = pm.PaymentMethodID
WHERE f.IsFraud = 1 OR f.RiskCategory IN ('Flagged Fraud', 'High-Value Transaction', 'Suspicious High-Value');
GO

PRINT 'Analytical SQL Views created successfully.';
GO
