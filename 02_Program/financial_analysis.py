#!/usr/bin/env python3
"""
Financial Analytics SQL Queries & Insights Generator
Project: Financial Transaction & Customer Analytics System
Domain: Financial Data Analytics
Author: Antigravity AI Pair Programmer
"""

import os
import sys
import sqlite3
import pandas as pd

def run_financial_analysis():
    print("==========================================================")
    print("   RUNNING FINANCIAL DATA ANALYTICS & INSIGHTS PIPELINE   ")
    print("==========================================================")

    db_path = '/Users/pranav/Downloads/Financial_Analytics/01_Database/FinancialAnalyticsDB.db'
    results_dir = '/Users/pranav/Downloads/Financial_Analytics/06_Results'
    os.makedirs(results_dir, exist_ok=True)
    results_file = os.path.join(results_dir, 'financial_analysis_results.txt')

    conn = sqlite3.connect(db_path)

    report_lines = []
    def log(text=""):
        print(text)
        report_lines.append(text)

    log("================================================================================")
    log("          FINANCIAL TRANSACTION & CUSTOMER ANALYTICS SYSTEM REPORT          ")
    log("================================================================================")
    log(f"Generated On: 2026-09-02")
    log(f"Database Engine: MS SQL Server / FinancialAnalyticsDB Database Engine")
    log("================================================================\n")

    # 1. Executive Summary KPI Metrics
    log("--- SECTION 1: EXECUTIVE FINANCIAL OVERVIEW ---")
    query_exec = """
        SELECT 
            COUNT(*) AS TotalTransactions,
            SUM(amount) AS TotalRevenue,
            AVG(amount) AS AvgTransactionValue,
            MIN(amount) AS MinTransaction,
            MAX(amount) AS MaxTransaction,
            COUNT(DISTINCT customer_id) AS ActiveCustomers,
            SUM(CASE WHEN is_fraud = 1 THEN 1 ELSE 0 END) AS TotalFraudCount,
            SUM(CASE WHEN is_fraud = 1 THEN amount ELSE 0 END) AS TotalFraudAmount
        FROM FactTransactions;
    """
    exec_df = pd.read_sql_query(query_exec, conn)
    tot_txns = exec_df['TotalTransactions'][0]
    tot_rev = exec_df['TotalRevenue'][0]
    avg_txn = exec_df['AvgTransactionValue'][0]
    act_cust = exec_df['ActiveCustomers'][0]
    fraud_cnt = exec_df['TotalFraudCount'][0]
    fraud_amt = exec_df['TotalFraudAmount'][0]

    log(f"Total Transactions Processed : {tot_txns:,}")
    log(f"Total Transaction Revenue    : ${tot_rev:,.2f}")
    log(f"Average Transaction Value    : ${avg_txn:,.2f}")
    log(f"Active Unique Customers      : {act_cust:,}")
    log(f"Total Flagged Fraud Txns     : {fraud_cnt:,} ({fraud_cnt/tot_txns*100:.2f}%)")
    log(f"Total Fraud Exposure Amount  : ${fraud_amt:,.2f}")
    log("")

    # 2. Customer Spending Analytics
    log("--- SECTION 2: TOP 10 HIGH-VALUE CUSTOMERS ---")
    query_cust = """
        SELECT 
            c.customer_id,
            c.full_name,
            c.gender,
            c.age,
            c.age_group,
            c.city,
            c.state,
            COUNT(f.transaction_id) AS TxnVolume,
            SUM(f.amount) AS TotalSpend,
            AVG(f.amount) AS AvgSpend
        FROM DimCustomers c
        JOIN FactTransactions f ON c.customer_id = f.customer_id
        GROUP BY c.customer_id, c.full_name, c.gender, c.age, c.age_group, c.city, c.state
        ORDER BY TotalSpend DESC
        LIMIT 10;
    """
    cust_df = pd.read_sql_query(query_cust, conn)
    log(cust_df.to_string(index=False))
    log("")

    # 3. Age Group & Gender Spending Breakdown
    log("--- SECTION 3: CUSTOMER DEMOGRAPHIC SPENDING MATRIX ---")
    query_demo = """
        SELECT 
            c.age_group,
            c.gender,
            COUNT(DISTINCT c.customer_id) AS CustomerCount,
            COUNT(f.transaction_id) AS TxnVolume,
            SUM(f.amount) AS TotalRevenue,
            AVG(f.amount) AS AvgSpend
        FROM DimCustomers c
        JOIN FactTransactions f ON c.customer_id = f.customer_id
        GROUP BY c.age_group, c.gender
        ORDER BY c.age_group, c.gender;
    """
    demo_df = pd.read_sql_query(query_demo, conn)
    log(demo_df.to_string(index=False))
    log("")

    # 4. Spending Category & Super Category Performance
    log("--- SECTION 4: CATEGORY & SUPER-CATEGORY REVENUE ANALYSIS ---")
    query_cat = """
        SELECT 
            cat.super_category,
            cat.category,
            COUNT(f.transaction_id) AS Volume,
            SUM(f.amount) AS Revenue,
            ROUND(SUM(f.amount) * 100.0 / (SELECT SUM(amount) FROM FactTransactions), 2) AS RevenueSharePct,
            AVG(f.amount) AS AvgTicketSize
        FROM DimCategories cat
        JOIN FactTransactions f ON cat.category_id = f.category_id
        GROUP BY cat.super_category, cat.category
        ORDER BY Revenue DESC;
    """
    cat_df = pd.read_sql_query(query_cat, conn)
    log(cat_df.to_string(index=False))
    log("")

    # 5. Payment Method Performance
    log("--- SECTION 5: PAYMENT METHOD PERFORMANCE & PREFERENCE ---")
    query_pay = """
        SELECT 
            pm.payment_method_name,
            pm.channel_type,
            COUNT(f.transaction_id) AS Volume,
            SUM(f.amount) AS TotalRevenue,
            AVG(f.amount) AS AvgAmount,
            SUM(CASE WHEN f.is_fraud = 1 THEN 1 ELSE 0 END) AS FraudCount
        FROM DimPaymentMethods pm
        JOIN FactTransactions f ON pm.payment_method_id = f.payment_method_id
        GROUP BY pm.payment_method_name, pm.channel_type
        ORDER BY TotalRevenue DESC;
    """
    pay_df = pd.read_sql_query(query_pay, conn)
    log(pay_df.to_string(index=False))
    log("")

    # 6. Geographic Distribution by Region & Top States
    log("--- SECTION 6: GEOGRAPHIC REVENUE BY US REGION & TOP 10 STATES ---")
    query_reg = """
        SELECT 
            l.region,
            COUNT(DISTINCT f.customer_id) AS UniqueCustomers,
            COUNT(f.transaction_id) AS Volume,
            SUM(f.amount) AS Revenue,
            AVG(f.amount) AS AvgSpend
        FROM DimLocations l
        JOIN FactTransactions f ON l.location_id = f.location_id
        GROUP BY l.region
        ORDER BY Revenue DESC;
    """
    reg_df = pd.read_sql_query(query_reg, conn)
    log("US REGIONAL BREAKDOWN:")
    log(reg_df.to_string(index=False))

    log("\nTOP 10 STATES BY REVENUE:")
    query_state = """
        SELECT 
            l.state,
            l.region,
            COUNT(f.transaction_id) AS Volume,
            SUM(f.amount) AS Revenue,
            AVG(f.amount) AS AvgSpend
        FROM DimLocations l
        JOIN FactTransactions f ON l.location_id = f.location_id
        GROUP BY l.state, l.region
        ORDER BY Revenue DESC
        LIMIT 10;
    """
    state_df = pd.read_sql_query(query_state, conn)
    log(state_df.to_string(index=False))
    log("")

    # 7. Risk & Anomaly Classification
    log("--- SECTION 7: RISK & ANOMALY CATEGORY BREAKDOWN ---")
    query_risk = """
        SELECT 
            risk_category,
            COUNT(transaction_id) AS TransactionCount,
            SUM(amount) AS TotalAmount,
            AVG(amount) AS AvgAmount,
            ROUND(COUNT(transaction_id) * 100.0 / (SELECT COUNT(*) FROM FactTransactions), 2) AS VolumePct
        FROM FactTransactions
        GROUP BY risk_category
        ORDER BY TotalAmount DESC;
    """
    risk_df = pd.read_sql_query(query_risk, conn)
    log(risk_df.to_string(index=False))
    log("")

    # Write report file
    with open(results_file, 'w') as f:
        f.write("\n".join(report_lines))

    conn.close()
    print(f"\nFinancial analytics report generated and saved to: {results_file}")

if __name__ == '__main__':
    run_financial_analysis()
