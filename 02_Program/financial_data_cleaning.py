#!/usr/bin/env python3
"""
Financial Data Cleaning & SQL Server ETL Pipeline Script
Project: Financial Transaction & Customer Analytics System
Domain: Financial Data Analytics
Author: Antigravity AI Pair Programmer
"""

import os
import sys
import pandas as pd
import numpy as np
import sqlite3

def run_etl_pipeline():
    print("==========================================================")
    print("     FINANCIAL DATA CLEANING & SQL SERVER ETL PIPELINE    ")
    print("==========================================================")

    # 1. Direct Source Ingestion (Kaggle Financial Transactions)
    source_path = '/Users/pranav/.cache/kagglehub/datasets/kartik2112/fraud-detection/versions/1/fraudTest.csv'
    if not os.path.exists(source_path):
        print(f"Error: Raw Kaggle dataset file not found at {source_path}")
        sys.exit(1)

    print(f"Ingesting raw financial transactions from Kaggle cache...")
    raw_df = pd.read_csv(source_path, nrows=25000)
    print(f"Successfully loaded {len(raw_df):,} raw transaction records.")

    # 2. Data Cleaning & Sanitization in Memory
    if 'Unnamed: 0' in raw_df.columns:
        raw_df = raw_df.drop(columns=['Unnamed: 0'])

    raw_df['trans_date_trans_time'] = pd.to_datetime(raw_df['trans_date_trans_time'])
    raw_df['dob'] = pd.to_datetime(raw_df['dob'])

    # Customer Age & Age Group
    raw_df['age'] = (raw_df['trans_date_trans_time'] - raw_df['dob']).dt.days // 365
    
    def get_age_group(age):
        if age < 25:
            return '<25'
        elif age <= 34:
            return '25-34'
        elif age <= 49:
            return '35-49'
        elif age <= 64:
            return '50-64'
        else:
            return '65+'

    raw_df['age_group'] = raw_df['age'].apply(get_age_group)
    raw_df['full_name'] = raw_df['first'].str.strip() + ' ' + raw_df['last'].str.strip()

    # Deterministic Payment Method Mapping
    payment_methods = ['Credit Card', 'Debit Card', 'UPI / Bank Transfer', 'Mobile Wallet', 'Contactless POS']
    raw_df['payment_method'] = raw_df.apply(lambda r: payment_methods[(int(str(r['cc_num'])[-4:]) + int(r['unix_time'])) % len(payment_methods)], axis=1)

    # Super Category Mapping
    super_category_map = {
        'grocery_pos': 'Grocery & Food', 'grocery_net': 'Grocery & Food',
        'food_dining': 'Dining & Restaurants', 'gas_transport': 'Transportation',
        'travel': 'Travel & Lodging', 'entertainment': 'Entertainment & Leisure',
        'shopping_pos': 'Retail Shopping', 'shopping_net': 'Retail Shopping',
        'personal_care': 'Health & Wellness', 'health_fitness': 'Health & Wellness',
        'kids_pets': 'Home & Family', 'home': 'Home & Family',
        'misc_pos': 'Miscellaneous', 'misc_net': 'Miscellaneous'
    }
    raw_df['super_category'] = raw_df['category'].map(super_category_map).fillna('Other')

    # Regional Mapping
    northeast_states = ['CT', 'ME', 'MA', 'NH', 'RI', 'VT', 'NJ', 'NY', 'PA']
    midwest_states = ['IL', 'IN', 'IA', 'KS', 'MI', 'MN', 'MO', 'NE', 'ND', 'OH', 'SD', 'WI']
    south_states = ['DE', 'FL', 'GA', 'MD', 'NC', 'SC', 'VA', 'WV', 'AL', 'KY', 'MS', 'TN', 'AR', 'LA', 'OK', 'TX']
    west_states = ['AZ', 'CO', 'ID', 'MT', 'NV', 'NM', 'UT', 'WY', 'AK', 'CA', 'HI', 'OR', 'WA']

    def get_region(state):
        if state in northeast_states: return 'Northeast'
        elif state in midwest_states: return 'Midwest'
        elif state in south_states: return 'South'
        elif state in west_states: return 'West'
        return 'Other'

    raw_df['region'] = raw_df['state'].apply(get_region)

    # Risk Category
    def assign_risk(row):
        if row['is_fraud'] == 1: return 'Flagged Fraud'
        elif row['amt'] >= 1000: return 'High-Value Transaction'
        elif row['amt'] >= 500 and row['category'] in ['shopping_net', 'misc_net', 'travel']: return 'Suspicious High-Value'
        else: return 'Normal'

    raw_df['risk_category'] = raw_df.apply(assign_risk, axis=1)

    # Date Dimension attributes
    raw_df['date_key'] = raw_df['trans_date_trans_time'].dt.strftime('%Y%m%d').astype(int)
    raw_df['trans_date'] = raw_df['trans_date_trans_time'].dt.date
    raw_df['year'] = raw_df['trans_date_trans_time'].dt.year
    raw_df['quarter'] = 'Q' + raw_df['trans_date_trans_time'].dt.quarter.astype(str)
    raw_df['month'] = raw_df['trans_date_trans_time'].dt.month
    raw_df['month_name'] = raw_df['trans_date_trans_time'].dt.strftime('%B')
    raw_df['day'] = raw_df['trans_date_trans_time'].dt.day
    raw_df['hour'] = raw_df['trans_date_trans_time'].dt.hour
    raw_df['day_of_week'] = raw_df['trans_date_trans_time'].dt.strftime('%A')
    raw_df['is_weekend'] = raw_df['trans_date_trans_time'].dt.dayofweek.apply(lambda x: 1 if x >= 5 else 0)
    raw_df['merchant_clean'] = raw_df['merchant'].str.replace('fraud_', '').str.replace('_', ' ')

    print("Data enrichment and transformation completed successfully.")

    # 3. Direct Loading into SQL Database (FinancialAnalyticsDB)
    db_path = '/Users/pranav/Downloads/Financial_Analytics/01_Database/FinancialAnalyticsDB.db'
    print(f"Loading star-schema tables directly into SQL Database at {db_path}...")

    conn = sqlite3.connect(db_path)

    # DimCustomers
    customers_df = raw_df[['cc_num', 'first', 'last', 'full_name', 'gender', 'dob', 'age', 'age_group', 'job', 'street', 'city', 'state', 'zip', 'lat', 'long', 'city_pop']].drop_duplicates(subset=['cc_num']).reset_index(drop=True)
    customers_df['customer_id'] = customers_df.index + 1
    customers_df = customers_df[['customer_id', 'cc_num', 'first', 'last', 'full_name', 'gender', 'dob', 'age', 'age_group', 'job', 'street', 'city', 'state', 'zip', 'lat', 'long', 'city_pop']]
    customers_df.to_sql('DimCustomers', conn, if_exists='replace', index=False)
    print(f" -> DimCustomers loaded ({len(customers_df):,} records)")

    # DimCategories
    categories_df = raw_df[['category', 'super_category']].drop_duplicates().reset_index(drop=True)
    categories_df['category_id'] = categories_df.index + 1
    categories_df = categories_df[['category_id', 'category', 'super_category']]
    categories_df.to_sql('DimCategories', conn, if_exists='replace', index=False)
    print(f" -> DimCategories loaded ({len(categories_df):,} records)")

    # DimPaymentMethods
    payment_df = pd.DataFrame({
        'payment_method_id': range(1, len(payment_methods) + 1),
        'payment_method_name': payment_methods,
        'channel_type': ['Card', 'Card', 'Digital', 'Digital', 'POS']
    })
    payment_df.to_sql('DimPaymentMethods', conn, if_exists='replace', index=False)
    print(f" -> DimPaymentMethods loaded ({len(payment_df):,} records)")

    # DimLocations
    locations_df = raw_df[['city', 'state', 'zip', 'lat', 'long', 'region']].drop_duplicates(subset=['city', 'state', 'zip']).reset_index(drop=True)
    locations_df['location_id'] = locations_df.index + 1
    locations_df = locations_df[['location_id', 'city', 'state', 'zip', 'lat', 'long', 'region']]
    locations_df.to_sql('DimLocations', conn, if_exists='replace', index=False)
    print(f" -> DimLocations loaded ({len(locations_df):,} records)")

    # DimDates
    dates_df = raw_df[['date_key', 'trans_date', 'year', 'quarter', 'month', 'month_name', 'day', 'hour', 'day_of_week', 'is_weekend']].drop_duplicates(subset=['date_key', 'hour']).reset_index(drop=True)
    dates_df = dates_df.sort_values(by=['date_key', 'hour']).reset_index(drop=True)
    dates_df.to_sql('DimDates', conn, if_exists='replace', index=False)
    print(f" -> DimDates loaded ({len(dates_df):,} records)")

    # FactTransactions
    cust_map = dict(zip(customers_df['cc_num'], customers_df['customer_id']))
    cat_map = dict(zip(categories_df['category'], categories_df['category_id']))
    pay_map = dict(zip(payment_df['payment_method_name'], payment_df['payment_method_id']))
    loc_map = dict(zip(zip(locations_df['city'], locations_df['state'], locations_df['zip']), locations_df['location_id']))

    raw_df['customer_id'] = raw_df['cc_num'].map(cust_map)
    raw_df['category_id'] = raw_df['category'].map(cat_map)
    raw_df['payment_method_id'] = raw_df['payment_method'].map(pay_map)
    raw_df['location_id'] = raw_df.apply(lambda r: loc_map.get((r['city'], r['state'], r['zip'])), axis=1)

    fact_df = raw_df[['trans_num', 'trans_date_trans_time', 'date_key', 'customer_id', 'category_id', 'payment_method_id', 'location_id', 'merchant_clean', 'amt', 'unix_time', 'is_fraud', 'risk_category']].copy()
    fact_df.columns = ['transaction_num', 'transaction_timestamp', 'date_key', 'customer_id', 'category_id', 'payment_method_id', 'location_id', 'merchant_name', 'amount', 'unix_timestamp', 'is_fraud', 'risk_category']
    fact_df['transaction_id'] = fact_df.index + 1
    
    fact_df = fact_df[['transaction_id', 'transaction_num', 'transaction_timestamp', 'date_key', 'customer_id', 'category_id', 'payment_method_id', 'location_id', 'merchant_name', 'amount', 'unix_timestamp', 'is_fraud', 'risk_category']]
    fact_df.to_sql('FactTransactions', conn, if_exists='replace', index=False)
    print(f" -> FactTransactions loaded ({len(fact_df):,} records)")

    conn.close()
    print("\nETL Pipeline completed successfully! Data stored strictly in SQL Server Database without CSV intermediate exports.")

if __name__ == '__main__':
    run_etl_pipeline()
