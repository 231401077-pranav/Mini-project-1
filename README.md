# Financial Transaction & Customer Analytics System

## 1. Project Overview
- **Project Title:** Financial Transaction & Customer Analytics System
- **Domain:** Financial Data Analytics
- **Database:** Microsoft SQL Server (`FinancialAnalyticsDB`)
- **Programming:** Python
- **Visualization:** Microsoft Power BI (Primary) and Tableau (Supplementary)
- **Dataset Size:** 25,000 transaction records

This project is an end-to-end financial data analytics system that analyzes transaction activity, customer spending, transaction categories, payment channels, geographical patterns, and fraud/risk indicators.

### Project Workflow
```text
Kaggle Dataset
      ↓
Python Data Cleaning & Transformation
      ↓
Microsoft SQL Server (FinancialAnalyticsDB)
      ↓
T-SQL Queries & Analytical Views
      ↓
Power BI / Tableau
      ↓
Business Insights & Results
```

---

## 2. Dataset Details
### Dataset Used
- **Kaggle Dataset:** Sparkov Financial Fraud Detection Dataset (`kartik2112/fraud-detection`)
- **Source:** Kaggle
- **Dataset Link:** [https://www.kaggle.com/datasets/kartik2112/fraud-detection](https://www.kaggle.com/datasets/kartik2112/fraud-detection)

From the original Kaggle dataset, **25,000 transaction records** were selected and processed for this mini project.

### Important Attributes
- Transaction number
- Transaction date and time
- Customer/card information
- Customer name, gender, date of birth, job
- City, state, ZIP code, latitude, longitude
- Merchant, transaction category, transaction amount, fraud indicator

> **Important Note:**  
> The original Kaggle dataset is used only as the source dataset for Python ingestion and preprocessing. The project database is Microsoft SQL Server. The submitted analytical workflow retrieves and analyzes data from SQL Server rather than depending on a CSV file.

---

## 3. Technologies Used
| Technology | Purpose |
| :--- | :--- |
| **Python** | Data cleaning, transformation, ETL and analysis |
| **Pandas** | Data processing |
| **NumPy** | Data transformation |
| **Microsoft SQL Server** | Primary data storage and management (`FinancialAnalyticsDB`) |
| **T-SQL** | Database operations, queries and analytical views |
| **Power BI Desktop** | Primary interactive visualization (5 pages) |
| **Tableau Desktop** | Supplementary visualization |
| **Jupyter Notebook** | Interactive analysis and demonstration |

---

## 4. Microsoft SQL Server Database
- **Database Name:** `FinancialAnalyticsDB`

The database contains a relational star-schema architecture.

### Main Tables
- `DimCustomers`
- `DimCategories`
- `DimPaymentMethods`
- `DimLocations`
- `DimDates`
- `FactTransactions`

### Fact Table (`FactTransactions`)
Contains the core financial transaction records: `TransactionID`, `DateKey`, `CustomerID`, `CategoryID`, `PaymentMethodID`, `LocationID`, `MerchantName`, `TransactionAmount`, `IsFraud`, `RiskCategory`.

### Dimension Tables
- `DimCustomers`: Customer demographic and profile information.
- `DimCategories`: Transaction categories and super-categories.
- `DimPaymentMethods`: Payment channels and channel classifications.
- `DimLocations`: City, state, ZIP code, coordinates and region.
- `DimDates`: Calendar attributes used for time-series analysis.

---

## 5. SQL Server Files
All SQL scripts are available in `01_Database/`:
1. **`01_FinancialDB_Create.sql`**: Creates `FinancialAnalyticsDB` database and configures environment.
2. **`02_FinancialDB_Tables.sql`**: Creates PKs, FKs, unique constraints, dimension tables, fact table, and supporting B-tree indexes.
3. **`03_FinancialDB_Insert.sql`**: Data insertion and loading verification process.
4. **`04_FinancialDB_Views.sql`**: Creates analytical views (`vw_ExecutiveOverview`, `vw_CustomerAnalytics`, `vw_CategoryPerformance`, `vw_GeographicDistribution`, `vw_RiskAndFraudAnalytics`).
5. **`05_FinancialDB_Queries.sql`**: Advanced T-SQL queries (Top customers, Categories, Revenue, Volume, Payment channels, State-wise performance, Fraud & High-value transactions).

---

## 6. Faculty SQL Interaction Guide
Faculty can execute SQL scripts in numerical order:
`01_FinancialDB_Create.sql` → `02_FinancialDB_Tables.sql` → `03_FinancialDB_Insert.sql` → `04_FinancialDB_Views.sql` → `05_FinancialDB_Queries.sql`

```sql
USE FinancialAnalyticsDB;
SELECT COUNT(*) AS TotalTransactions FROM FactTransactions; -- Expected: 25,000
```

---

## 7. Power BI Dashboard (Primary Visualization Tool)
- **Power BI File:** `03_PowerBI/Financial_Analytics.pbix`
- **Interactive Presentation:** `03_PowerBI/Financial_Analytics_Dashboard.html`
- **DAX Measure Library:** `03_PowerBI/dax_measures.dax`

### 5 Dashboard Pages
- **Page 1 — Executive Financial Overview:** Total Revenue, Total Volume, Avg Value, Active Customers, Monthly Trend.
- **Page 2 — Customer Analytics:** Customer spending, ranking, top 10 leaderboard, transaction frequency, age-group breakdown.
- **Page 3 — Transaction & Category Analytics:** Category revenue, volume, payment-channel analysis, ticket sizes.
- **Page 4 — Geographical Analytics:** State-wise revenue, city performance, regional distribution.
- **Page 5 — Risk & Anomaly Analytics:** Fraud cases, fraud exposure amount, high-value transaction outliers, risk logs.

---

## 8. Tableau (Supplementary BI Asset)
- **Tableau Workbook:** `04_Tableau/Financial_Analytics.twbx`
- **Calculation Guide:** `04_Tableau/tableau_calculations.md`

---

## 9. Python Program Files
All programs are available in `02_Program/`:
- `financial_data_cleaning.py`: Ingestion, cleaning, transformation, and star-schema loading into SQL.
- `load_financial_data_to_sqlserver.py`: Database engine verification.
- `validate_financial_data.py`: Automated quality tests (nulls, PK/FK, orphans, range checks).
- `financial_analysis.py`: Analytical execution against SQL Server database.
- `financial_analysis.ipynb`: Interactive Jupyter Notebook.

---

## 10. Project Results
| KPI | Result |
| :--- | :--- |
| **Total Transactions** | 25,000 |
| **Total Transaction Value** | $1,724,423.32 |
| **Average Transaction Value** | $68.98 |
| **Active Customers** | 909 |
| **Fraud Cases** | 83 |
| **Fraud Exposure** | $47,788.71 |
| **Top Category** | `grocery_pos` |
| **Top State** | Texas (TX) |

---

## 11. Documentation
Academic Word Report: `05_Documentation/Financial_Analytics_Project_Report.docx`  
Contains required academic sections: **Aim, Algorithm, Methodology, Dataset Details, Results, and Observations**.

---

## 12. QR Code
Independent QR Code: `07_QR/Financial_Analytics_QR.png`  
Provides exclusive access to Project 1 resources.

---

## 13. Submission Statement
This project is an independent Financial Data Analytics mini project. It uses approximately 20,000+ financial transaction records, stores and manages the analytical data in Microsoft SQL Server, performs data analysis using Python and T-SQL, and presents business insights through Power BI and Tableau.

The project is maintained independently from the second mini project and has its own documentation, program files, database scripts, BI assets, results and QR verification mechanism.
