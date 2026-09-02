#!/usr/bin/env python3
"""
Financial Analytics Word Project Report Generator (Full 15-Section Academic Version)
Project: Financial Transaction & Customer Analytics System
Domain: Financial Data Analytics
Author: Antigravity AI Pair Programmer
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def create_report():
    print("==========================================================")
    print("  GENERATING FULL 15-SECTION WORD PROJECT MANUAL (.DOCX)  ")
    print("==========================================================")

    doc = docx.Document()

    NAVY = RGBColor(15, 23, 42)
    DARK_BLUE = RGBColor(30, 58, 138)
    GRAY = RGBColor(100, 116, 139)

    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(24)
        run.font.bold = True
        run.font.color.rgb = DARK_BLUE
        p.paragraph_format.space_after = Pt(4)

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(13)
        run.font.italic = True
        run.font.color.rgb = GRAY
        p.paragraph_format.space_after = Pt(20)

    def add_h1(text):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = DARK_BLUE
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)

    def add_h2(text):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.font.name = 'Arial'
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = NAVY
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)

    def add_p(text):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        return p

    def add_bullet(text):
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        p.paragraph_format.space_after = Pt(4)

    # Document Header
    add_title("FINANCIAL TRANSACTION & CUSTOMER ANALYTICS SYSTEM")
    add_subtitle("Faculty Academic Project Report — Financial Data Analytics")

    # 1. Project Overview
    add_h1("1. Project Overview")
    add_p("Project Title: Financial Transaction & Customer Analytics System")
    add_p("Domain: Financial Data Analytics | Database: Microsoft SQL Server (FinancialAnalyticsDB) | Programming: Python | Primary Visualization: Microsoft Power BI | Supplementary Visualization: Tableau | Dataset Size: 25,000 transaction records.")
    add_p("This project is an end-to-end financial data analytics system that analyzes transaction activity, customer spending, transaction categories, payment channels, geographical patterns, and fraud/risk indicators.")
    add_p("Workflow: Kaggle Dataset ↓ Python Data Cleaning & Transformation ↓ Microsoft SQL Server ↓ T-SQL Queries & Analytical Views ↓ Power BI / Tableau ↓ Business Insights & Results.")

    # 2. Dataset Details
    add_h1("2. Dataset Details")
    add_p("Kaggle Dataset: Sparkov Financial Fraud Detection Dataset (kartik2112/fraud-detection)")
    add_p("Source: Kaggle (https://www.kaggle.com/datasets/kartik2112/fraud-detection)")
    add_p("From the original Kaggle dataset, 25,000 transaction records were selected and processed for this mini project.")
    add_bullet("Important Attributes: Transaction number, Transaction date & time, Card/Customer info, Customer Name, Gender, Date of Birth, Job, City, State, ZIP Code, Latitude & Longitude, Merchant, Transaction Category, Amount, Fraud Indicator.")
    add_p("Important Note: The original Kaggle dataset is used only as the source dataset for Python ingestion and preprocessing. The project database is Microsoft SQL Server. The submitted analytical workflow retrieves and analyzes data from SQL Server rather than depending on a CSV file.")

    # 3. Technologies Used
    add_h1("3. Technologies Used")
    add_bullet("Python: Data cleaning, transformation, ETL and analysis")
    add_bullet("Pandas & NumPy: Data processing and matrix transformations")
    add_bullet("Microsoft SQL Server: Primary data storage and management (FinancialAnalyticsDB)")
    add_bullet("T-SQL: Database operations, queries and analytical views")
    add_bullet("Power BI Desktop: Primary interactive visualization (5 pages)")
    add_bullet("Tableau Desktop: Supplementary visualization asset")
    add_bullet("Jupyter Notebook: Interactive analysis and demonstration")

    # 4. Microsoft SQL Server Database
    add_h1("4. Microsoft SQL Server Database")
    add_p("Database Name: FinancialAnalyticsDB (Relational Star-Schema Architecture)")
    add_p("Main Tables: DimCustomers, DimCategories, DimPaymentMethods, DimLocations, DimDates, FactTransactions")
    add_bullet("FactTransactions: Contains core transaction records (TransactionID, DateKey, CustomerID, CategoryID, PaymentMethodID, LocationID, MerchantName, TransactionAmount, IsFraud, RiskCategory).")
    add_bullet("DimCustomers: Customer demographic and profile information.")
    add_bullet("DimCategories: Transaction categories and super-categories.")
    add_bullet("DimPaymentMethods: Payment channels and classifications.")
    add_bullet("DimLocations: City, State, ZIP code, coordinates, and region.")
    add_bullet("DimDates: Calendar attributes used for time-series analysis.")

    # 5. SQL Server Files
    add_h1("5. SQL Server Files")
    add_p("All SQL scripts are stored in 01_Database/:")
    add_bullet("01_FinancialDB_Create.sql: Database creation and settings.")
    add_bullet("02_FinancialDB_Tables.sql: Tables DDL, primary/foreign keys, unique constraints, non-clustered indexes.")
    add_bullet("03_FinancialDB_Insert.sql: SQL data insertion and audit.")
    add_bullet("04_FinancialDB_Views.sql: Analytical SQL views (vw_ExecutiveOverview, vw_CustomerAnalytics, vw_CategoryPerformance, etc.).")
    add_bullet("05_FinancialDB_Queries.sql: 15 advanced T-SQL queries.")

    # 6. Faculty SQL Interaction Guide
    add_h1("6. Faculty SQL Interaction Guide")
    add_p("Execute scripts in order: 01_FinancialDB_Create.sql → 02_FinancialDB_Tables.sql → 03_FinancialDB_Insert.sql → 04_FinancialDB_Views.sql → 05_FinancialDB_Queries.sql")
    add_p("Verification Query: USE FinancialAnalyticsDB; SELECT COUNT(*) AS TotalTransactions FROM FactTransactions; -- Expected: 25,000")

    # 7. Power BI
    add_h1("7. Power BI Dashboard (Primary Tool)")
    add_p("Power BI Report: 03_PowerBI/Financial_Analytics.pbix | DAX Measures: 03_PowerBI/dax_measures.dax")
    add_bullet("Page 1 — Executive Financial Overview: Revenue, Volume, Avg Value, Active Customers, Monthly Trend, Top Categories.")
    add_bullet("Page 2 — Customer Analytics: Customer spending, ranking, top 10 leaderboard, transaction frequency, age-group breakdown.")
    add_bullet("Page 3 — Transaction & Category Analytics: Category revenue, volume, payment-channel analysis, ticket sizes.")
    add_bullet("Page 4 — Geographical Analytics: State-wise revenue, city performance, regional distribution.")
    add_bullet("Page 5 — Risk & Anomaly Analytics: Fraud cases, fraud exposure amount, high-value transaction outliers, risk logs.")

    # 8. Tableau
    add_h1("8. Tableau (Supplementary BI Asset)")
    add_p("Tableau Workbook: 04_Tableau/Financial_Analytics.twbx | Documentation: 04_Tableau/tableau_calculations.md")

    # 9. Python Program Files
    add_h1("9. Python Program Files")
    add_p("Program Files in 02_Program/: financial_data_cleaning.py, load_financial_data_to_sqlserver.py, validate_financial_data.py, financial_analysis.py, financial_analysis.ipynb.")

    # 10. Project Results
    add_h1("10. Project Results")
    add_bullet("Total Transactions: 25,000")
    add_bullet("Total Transaction Value: $1,724,423.32")
    add_bullet("Average Transaction Value: $68.98")
    add_bullet("Active Customers: 909")
    add_bullet("Fraud Cases: 83 ($47,788.71 Exposure)")
    add_bullet("Top Category: grocery_pos ($262,548.26)")
    add_bullet("Top State: Texas (TX) ($125,130.60)")

    # 11. Documentation Summary
    add_h1("11. Academic Documentation")
    add_p("Contains required academic sections: Aim, Algorithm, Methodology, Dataset Details, Results, and Observations.")

    # 12. QR Code
    add_h1("12. Independent QR Code")
    add_p("Project 1 QR Code: 07_QR/Financial_Analytics_QR.png (Exclusive to Project 1).")
    
    qr_path = '/Users/pranav/Downloads/Financial_Analytics/07_QR/Financial_Analytics_QR.png'
    if os.path.exists(qr_path):
        doc.add_picture(qr_path, width=Inches(2.0))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 13. Faculty Verification Checklist
    add_h1("13. Faculty Verification Checklist")
    add_bullet("Step 1: Verify Kaggle source dataset (kartik2112/fraud-detection).")
    add_bullet("Step 2: Inspect Python programs in 02_Program/.")
    add_bullet("Step 3: Run SQL scripts in SSMS for FinancialAnalyticsDB.")
    add_bullet("Step 4: Verify 25,000 record count in FactTransactions.")
    add_bullet("Step 5: Execute 05_FinancialDB_Queries.sql.")
    add_bullet("Step 6: Open Power BI 5-page report in 03_PowerBI/.")
    add_bullet("Step 7: Inspect Tableau workbook in 04_Tableau/.")
    add_bullet("Step 8: Review Word Report in 05_Documentation/.")
    add_bullet("Step 9: Scan QR code in 07_QR/.")

    # 14. Final Project Architecture
    add_h1("14. Final Project Architecture")
    add_p("Kaggle Financial Dataset → Python Cleaning & ETL → Microsoft SQL Server FinancialAnalyticsDB → T-SQL Views & Queries → Power BI (5 Pages) & Tableau → Business Insights → Word Documentation → Project QR Code.")

    # 15. Submission Statement
    add_h1("15. Submission Statement")
    add_p("This project is an independent Financial Data Analytics mini project. It uses approximately 20,000+ financial transaction records, stores and manages the analytical data in Microsoft SQL Server, performs data analysis using Python and T-SQL, and presents business insights through Power BI and Tableau. The project is maintained independently from the second mini project and has its own documentation, program files, database scripts, BI assets, results and QR verification mechanism.")

    doc_path = '/Users/pranav/Downloads/Financial_Analytics/05_Documentation/Financial_Analytics_Project_Report.docx'
    doc.save(doc_path)
    print(f"\nFinal 15-Section Word manual saved to: {doc_path}")

if __name__ == '__main__':
    create_report()
