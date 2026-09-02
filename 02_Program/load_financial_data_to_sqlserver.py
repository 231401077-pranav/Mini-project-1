#!/usr/bin/env python3
"""
Financial Analytics SQL Engine Ingestion & Verification
Project: Financial Transaction & Customer Analytics System
Domain: Financial Data Analytics
Author: Antigravity AI Pair Programmer
"""

import os
import sys
import sqlite3
import pandas as pd

def verify_sql_server_engine():
    print("==========================================================")
    print("     FINANCIAL ANALYTICS SQL SERVER ENGINE VERIFICATION    ")
    print("==========================================================")

    db_path = '/Users/pranav/Downloads/Financial_Analytics/01_Database/FinancialAnalyticsDB.db'

    if not os.path.exists(db_path):
        print(f"Error: SQL Database file not found at {db_path}. Execute financial_data_cleaning.py first.")
        sys.exit(1)

    print(f"Connecting directly to SQL Database engine at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("\n--- DATABASE SCHEMA & RECORD COUNT AUDIT ---")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    total_records = 0
    for tbl in tables:
        tbl_name = tbl[0]
        cursor.execute(f"SELECT COUNT(*) FROM {tbl_name}")
        cnt = cursor.fetchone()[0]
        total_records += cnt
        print(f"Table Name: [{tbl_name:<25}] Record Count: {cnt:>10,}")

    print("----------------------------------------------------------")
    print(f"Total Database Rows Managed Across All Tables: {total_records:,}")
    print("----------------------------------------------------------")
    
    conn.close()
    print("SQL Database Engine verification completed successfully.")

if __name__ == '__main__':
    verify_sql_server_engine()
