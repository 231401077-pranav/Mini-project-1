#!/usr/bin/env python3
"""
Financial Analytics Data Quality Validation Script
Project: Financial Transaction & Customer Analytics System
Domain: Financial Data Analytics
Author: Antigravity AI Pair Programmer
"""

import os
import sys
import sqlite3
import pandas as pd

def validate_data_quality():
    print("==========================================================")
    print("       FINANCIAL DATA QUALITY VALIDATION SUITE          ")
    print("==========================================================")

    db_path = '/Users/pranav/Downloads/Financial_Analytics/01_Database/FinancialAnalyticsDB.db'
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    tests_passed = 0
    total_tests = 0

    # Test 1: Record Count Check
    total_tests += 1
    cursor.execute("SELECT COUNT(*) FROM FactTransactions;")
    fact_count = cursor.fetchone()[0]
    print(f"\n[Test 1] Fact Table Record Count: {fact_count:,}")
    if fact_count >= 20000:
        print(" -> PASS: Fact table contains >= 20,000 records.")
        tests_passed += 1
    else:
        print(" -> FAIL: Fact table contains less than 20,000 records.")

    # Test 2: Foreign Key Integrity Check (Customer ID)
    total_tests += 1
    cursor.execute("""
        SELECT COUNT(*) FROM FactTransactions f 
        LEFT JOIN DimCustomers c ON f.customer_id = c.customer_id 
        WHERE c.customer_id IS NULL;
    """)
    orphan_cust = cursor.fetchone()[0]
    print(f"[Test 2] Orphan Customer Foreign Keys: {orphan_cust}")
    if orphan_cust == 0:
        print(" -> PASS: 100% Customer Foreign Key Integrity.")
        tests_passed += 1
    else:
        print(" -> FAIL: Orphan Customer Keys detected!")

    # Test 3: Foreign Key Integrity Check (Category ID)
    total_tests += 1
    cursor.execute("""
        SELECT COUNT(*) FROM FactTransactions f 
        LEFT JOIN DimCategories cat ON f.category_id = cat.category_id 
        WHERE cat.category_id IS NULL;
    """)
    orphan_cat = cursor.fetchone()[0]
    print(f"[Test 3] Orphan Category Foreign Keys: {orphan_cat}")
    if orphan_cat == 0:
        print(" -> PASS: 100% Category Foreign Key Integrity.")
        tests_passed += 1
    else:
        print(" -> FAIL: Orphan Category Keys detected!")

    # Test 4: Missing / Null Value Audit in Fact Table
    total_tests += 1
    cursor.execute("""
        SELECT COUNT(*) FROM FactTransactions 
        WHERE amount IS NULL OR transaction_num IS NULL OR customer_id IS NULL OR date_key IS NULL;
    """)
    null_count = cursor.fetchone()[0]
    print(f"[Test 4] Null / Missing Key Values: {null_count}")
    if null_count == 0:
        print(" -> PASS: Zero nulls in primary transaction attributes.")
        tests_passed += 1
    else:
        print(" -> FAIL: Missing key values found!")

    # Test 5: Transaction Amount Range Audit
    total_tests += 1
    cursor.execute("SELECT MIN(amount), MAX(amount), AVG(amount) FROM FactTransactions;")
    min_amt, max_amt, avg_amt = cursor.fetchone()
    print(f"[Test 5] Amount Range Check: Min=${min_amt:,.2f}, Max=${max_amt:,.2f}, Avg=${avg_amt:,.2f}")
    if min_amt > 0 and max_amt > min_amt:
        print(" -> PASS: Transaction amounts are within valid positive bounds.")
        tests_passed += 1
    else:
        print(" -> FAIL: Invalid transaction amounts detected!")

    # Test 6: Risk & Fraud Flag Validation
    total_tests += 1
    cursor.execute("SELECT COUNT(*) FROM FactTransactions WHERE is_fraud = 1;")
    fraud_cnt = cursor.fetchone()[0]
    print(f"[Test 6] Flagged Fraud Count: {fraud_cnt}")
    if fraud_cnt > 0:
        print(" -> PASS: Fraud anomalies correctly identified.")
        tests_passed += 1
    else:
        print(" -> FAIL: No fraud transactions found.")

    conn.close()

    print("\n==========================================================")
    print(f" VALIDATION SUMMARY: {tests_passed}/{total_tests} TESTS PASSED ({tests_passed/total_tests*100:.1f}%)")
    print("==========================================================")

if __name__ == '__main__':
    validate_data_quality()
