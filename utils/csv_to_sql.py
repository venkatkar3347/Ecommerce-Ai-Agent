import pandas as pd
import sqlite3
import os

def convert_csv_to_sql():
    # Ensure db folder exists
    os.makedirs("db", exist_ok=True)
    
    # Load CSVs
    try:
        ads = pd.read_csv('data/Product_Level_Ad_Sales.csv')
        sales = pd.read_csv('data/Product_Level_Total_Sales.csv')
        eligibility = pd.read_csv('data/Product_Level_Eligibility.csv')
        
        # Connect to SQLite
        conn = sqlite3.connect('db/ecommerce.db')
        
        # Write to SQLite
        ads.to_sql('ad_sales', conn, if_exists='replace', index=False)
        sales.to_sql('total_sales', conn, if_exists='replace', index=False)
        eligibility.to_sql('eligibility', conn, if_exists='replace', index=False)
        
        conn.close()
        print("CSVs successfully converted to SQLite database.")
    except Exception as e:
        print(f"Error converting CSVs to SQLite: {e}")

if __name__ == "__main__":
    convert_csv_to_sql()