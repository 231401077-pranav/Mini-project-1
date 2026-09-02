-- ============================================================================
-- SQL Script 1: Financial Analytics Database Creation
-- Database Name: FinancialAnalyticsDB
-- RDBMS Engine: Microsoft SQL Server (T-SQL)
-- Project: Financial Transaction & Customer Analytics System
-- ============================================================================

USE master;
GO

-- Drop database if it exists to allow clean re-execution
IF EXISTS (SELECT * FROM sys.databases WHERE name = N'FinancialAnalyticsDB')
BEGIN
    ALTER DATABASE FinancialAnalyticsDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE FinancialAnalyticsDB;
END;
GO

-- Create FinancialAnalyticsDB
CREATE DATABASE FinancialAnalyticsDB;
GO

USE FinancialAnalyticsDB;
GO

PRINT 'FinancialAnalyticsDB created successfully.';
GO
