-- ============================================================================
-- SQL Script 2: Financial Analytics Schema & Table Definitions (Star Schema)
-- Database Name: FinancialAnalyticsDB
-- RDBMS Engine: Microsoft SQL Server (T-SQL)
-- Project: Financial Transaction & Customer Analytics System
-- ============================================================================

USE FinancialAnalyticsDB;
GO

-- 1. DimCustomers Table
IF OBJECT_ID('dbo.DimCustomers', 'U') IS NOT NULL DROP TABLE dbo.DimCustomers;
CREATE TABLE dbo.DimCustomers (
    CustomerID INT PRIMARY KEY IDENTITY(1,1),
    CardNumber BIGINT NOT NULL UNIQUE,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    FullName VARCHAR(100) NOT NULL,
    Gender CHAR(1) NOT NULL,
    DateOfBirth DATE NOT NULL,
    Age INT NOT NULL,
    AgeGroup VARCHAR(20) NOT NULL,
    JobTitle VARCHAR(100) NULL,
    StreetAddress VARCHAR(150) NULL,
    City VARCHAR(50) NOT NULL,
    State CHAR(2) NOT NULL,
    ZipCode INT NOT NULL,
    Latitude DECIMAL(9,6) NULL,
    Longitude DECIMAL(9,6) NULL,
    CityPopulation INT NULL
);
GO

-- 2. DimCategories Table
IF OBJECT_ID('dbo.DimCategories', 'U') IS NOT NULL DROP TABLE dbo.DimCategories;
CREATE TABLE dbo.DimCategories (
    CategoryID INT PRIMARY KEY IDENTITY(1,1),
    CategoryName VARCHAR(50) NOT NULL UNIQUE,
    SuperCategory VARCHAR(50) NOT NULL
);
GO

-- 3. DimPaymentMethods Table
IF OBJECT_ID('dbo.DimPaymentMethods', 'U') IS NOT NULL DROP TABLE dbo.DimPaymentMethods;
CREATE TABLE dbo.DimPaymentMethods (
    PaymentMethodID INT PRIMARY KEY IDENTITY(1,1),
    PaymentMethodName VARCHAR(50) NOT NULL UNIQUE,
    ChannelType VARCHAR(30) NOT NULL
);
GO

-- 4. DimLocations Table
IF OBJECT_ID('dbo.DimLocations', 'U') IS NOT NULL DROP TABLE dbo.DimLocations;
CREATE TABLE dbo.DimLocations (
    LocationID INT PRIMARY KEY IDENTITY(1,1),
    City VARCHAR(50) NOT NULL,
    State CHAR(2) NOT NULL,
    ZipCode INT NOT NULL,
    Latitude DECIMAL(9,6) NULL,
    Longitude DECIMAL(9,6) NULL,
    Region VARCHAR(30) NOT NULL,
    CONSTRAINT UQ_Location UNIQUE (City, State, ZipCode)
);
GO

-- 5. DimDates Table
IF OBJECT_ID('dbo.DimDates', 'U') IS NOT NULL DROP TABLE dbo.DimDates;
CREATE TABLE dbo.DimDates (
    DateKey INT NOT NULL,
    Hour INT NOT NULL,
    TransactionDate DATE NOT NULL,
    Year INT NOT NULL,
    Quarter CHAR(2) NOT NULL,
    Month INT NOT NULL,
    MonthName VARCHAR(15) NOT NULL,
    Day INT NOT NULL,
    DayOfWeek VARCHAR(15) NOT NULL,
    IsWeekend BIT NOT NULL,
    PRIMARY KEY (DateKey, Hour)
);
GO

-- 6. FactTransactions Table
IF OBJECT_ID('dbo.FactTransactions', 'U') IS NOT NULL DROP TABLE dbo.FactTransactions;
CREATE TABLE dbo.FactTransactions (
    TransactionID INT PRIMARY KEY IDENTITY(1,1),
    TransactionNum VARCHAR(64) NOT NULL UNIQUE,
    TransactionTimestamp DATETIME2 NOT NULL,
    DateKey INT NOT NULL,
    CustomerID INT NOT NULL,
    CategoryID INT NOT NULL,
    PaymentMethodID INT NOT NULL,
    LocationID INT NOT NULL,
    MerchantName VARCHAR(100) NOT NULL,
    TransactionAmount DECIMAL(12,2) NOT NULL,
    UnixTimestamp BIGINT NOT NULL,
    IsFraud BIT NOT NULL DEFAULT 0,
    RiskCategory VARCHAR(30) NOT NULL,
    CONSTRAINT FK_Fact_Customer FOREIGN KEY (CustomerID) REFERENCES dbo.DimCustomers(CustomerID),
    CONSTRAINT FK_Fact_Category FOREIGN KEY (CategoryID) REFERENCES dbo.DimCategories(CategoryID),
    CONSTRAINT FK_Fact_PaymentMethod FOREIGN KEY (PaymentMethodID) REFERENCES dbo.DimPaymentMethods(PaymentMethodID),
    CONSTRAINT FK_Fact_Location FOREIGN KEY (LocationID) REFERENCES dbo.DimLocations(LocationID)
);
GO

-- Create Non-Clustered Indexes for High-Performance Querying
CREATE NONCLUSTERED INDEX IX_Fact_DateKey ON dbo.FactTransactions(DateKey);
CREATE NONCLUSTERED INDEX IX_Fact_CustomerID ON dbo.FactTransactions(CustomerID);
CREATE NONCLUSTERED INDEX IX_Fact_CategoryID ON dbo.FactTransactions(CategoryID);
CREATE NONCLUSTERED INDEX IX_Fact_PaymentMethodID ON dbo.FactTransactions(PaymentMethodID);
CREATE NONCLUSTERED INDEX IX_Fact_LocationID ON dbo.FactTransactions(LocationID);
CREATE NONCLUSTERED INDEX IX_Fact_IsFraud ON dbo.FactTransactions(IsFraud);
CREATE NONCLUSTERED INDEX IX_Fact_RiskCategory ON dbo.FactTransactions(RiskCategory);
GO

PRINT 'Financial Analytics Star Schema tables and indexes created successfully.';
GO
