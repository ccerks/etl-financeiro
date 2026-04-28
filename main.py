import pandas as pd
import requests
import os
import yfinance as yf
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def send_webhook_alert(error_msg, function_name):
    """Sends an alert to a webhook (Discord/Slack) when a failure occurs."""
    webhook_url = os.getenv("WEBHOOK_URL")
    
    if not webhook_url:
        print("⚠️ WEBHOOK_URL not found. Skipping alert notification.")
        return

    # Payload formatted for Discord (Markdown supported)
    payload = {
        "content": f"🚨 **ETL Pipeline Alert** 🚨\n**Function:** `{function_name}`\n**Error:** `{error_msg}`\n**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    }

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("📲 Webhook alert sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send webhook alert: {e}")

def extract_crypto_data():
    """Extracts cryptocurrency data from CoinGecko API using a single batch request."""
    assets = ['bitcoin', 'ethereum', 'solana', 'cardano']
    assets_joined = ','.join(assets)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={assets_joined}&vs_currencies=usd"
    data_list = []
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        for asset in assets:
            if asset in data:
                data_list.append({
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'asset': asset,
                    'price_usd': data[asset]['usd']
                })
    except Exception as e:
        error_details = f"HTTP Request failed for Crypto API: {e}"
        print(f"❌ {error_details}")
        send_webhook_alert(error_details, "extract_crypto_data")
            
    return pd.DataFrame(data_list)

def extract_traditional_markets():
    """Extracts daily closing prices for traditional assets via Yahoo Finance."""
    assets = {"SPY": "S&P 500", "GLD": "Gold"}
    data_list = []

    for symbol, name in assets.items():
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")
            if not hist.empty:
                data_list.append({
                    "date": hist.index[-1].strftime('%Y-%m-%d'),
                    "asset": name,
                    "price_usd": float(hist["Close"].iloc[-1])
                })
        except Exception as e:
            error_details = f"YFinance failed for {name} ({symbol}): {e}"
            print(f"❌ {error_details}")
            send_webhook_alert(error_details, "extract_traditional_markets")

    return pd.DataFrame(data_list)

def validate_data_quality(df, source_name):
    """
    Validates data quality: uniqueness, completeness, and logical volume.
    Filters out bad records and triggers an alert if anomalies are detected.
    """
    if df.empty:
        print(f"⚠️ Validation skipped: No data received from {source_name}.")
        return df
        
    initial_count = len(df)
    
    # 1. Uniqueness: Drop duplicate combinations of Date + Asset
    df_clean = df.drop_duplicates(subset=['date', 'asset'])
    
    # 2. Completeness: Remove rows where price_usd is NaN/Null
    df_clean = df_clean.dropna(subset=['price_usd'])
    
    # 3. Volume Logic: Prices must be strictly positive
    df_clean = df_clean[df_clean['price_usd'] > 0]
    
    final_count = len(df_clean)
    
    # Alert if data was dropped during quality checks
    if final_count < initial_count:
        dropped_rows = initial_count - final_count
        warning_msg = f"Data Quality Warning: Dropped {dropped_rows} invalid row(s) from {source_name}."
        print(f"⚠️ {warning_msg}")
        send_webhook_alert(warning_msg, "validate_data_quality")
        
    if df_clean.empty:
        error_msg = f"Data Quality Failure: All records from {source_name} failed validation."
        print(f"❌ {error_msg}")
        send_webhook_alert(error_msg, "validate_data_quality")
        return pd.DataFrame() # Return empty to prevent database load
        
    print(f"✅ Data Quality Check passed for {source_name}.")
    return df_clean

def load_to_database(df, table_name):
    """Loads DataFrame to PostgreSQL Cloud Database."""
    if df.empty:
        print(f"⚠️ No data to load for {table_name}.")
        return

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not found in environment variables.")
    
    try:
        engine = create_engine(db_url)
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"✅ Data successfully pushed to table: {table_name}")
    except Exception as e:
        error_details = f"Database insertion failed for {table_name}: {e}"
        print(f"❌ {error_details}")
        send_webhook_alert(error_details, f"load_to_database ({table_name})")

if __name__ == "__main__":
    print("🚀 Starting Cloud-Native ETL Pipeline with Data Quality Checks...")
    
    # 1. Extraction (Bronze Layer)
    df_crypto_raw = extract_crypto_data()
    df_traditional_raw = extract_traditional_markets()
    
    # 2. Transformation & Quality Assurance (Silver Layer)
    df_crypto_clean = validate_data_quality(df_crypto_raw, "Crypto API")
    df_traditional_clean = validate_data_quality(df_traditional_raw, "Traditional Markets API")
    
    # 3. Load (Gold Layer Storage)
    if not df_crypto_clean.empty:
        load_to_database(df_crypto_clean, 'crypto_prices')
        
    if not df_traditional_clean.empty:
        load_to_database(df_traditional_clean, 'traditional_markets')
    
    print("🏁 Pipeline execution completed.")