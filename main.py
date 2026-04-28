import pandas as pd
import requests
import os
import yfinance as yf
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError

load_dotenv()

# --- 🛡️ DATA CONTRACTS (PYDANTIC) ---
class MarketDataContract(BaseModel):
    """Strict schema definition for incoming financial data."""
    date: str
    asset: str
    price_usd: float = Field(gt=0, description="Price must be strictly positive")

def send_webhook_alert(error_msg, function_name):
    """Sends an alert to a webhook (Discord/Slack) when a failure occurs."""
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        return

    payload = {
        "content": f"🚨 **ETL Pipeline Alert** 🚨\n**Function:** `{function_name}`\n**Error:** `{error_msg}`\n**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    }

    try:
        requests.post(webhook_url, json=payload)
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
                try:
                    # Validate against the Data Contract
                    valid_record = MarketDataContract(
                        date=datetime.now().strftime('%Y-%m-%d'),
                        asset=asset,
                        price_usd=data[asset]['usd']
                    )
                    data_list.append(valid_record.model_dump())
                except ValidationError as e:
                    error_msg = f"Schema Violation for {asset}: {e.errors()}"
                    print(f"❌ {error_msg}")
                    send_webhook_alert(error_msg, "extract_crypto_data (Pydantic)")
                    
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
                try:
                    # Validate against the Data Contract
                    valid_record = MarketDataContract(
                        date=hist.index[-1].strftime('%Y-%m-%d'),
                        asset=name,
                        price_usd=float(hist["Close"].iloc[-1])
                    )
                    data_list.append(valid_record.model_dump())
                except ValidationError as e:
                    error_msg = f"Schema Violation for {name}: {e.errors()}"
                    print(f"❌ {error_msg}")
                    send_webhook_alert(error_msg, "extract_traditional_markets (Pydantic)")
        except Exception as e:
            error_details = f"YFinance failed for {name} ({symbol}): {e}"
            print(f"❌ {error_details}")
            send_webhook_alert(error_details, "extract_traditional_markets")

    return pd.DataFrame(data_list)

def validate_data_quality(df, source_name):
    """
    Validates dataset-level quality. 
    Row-level typing and null-checks are already handled by Pydantic.
    """
    if df.empty:
        return df
        
    initial_count = len(df)
    
    # Dataset-level rule: Uniqueness
    df_clean = df.drop_duplicates(subset=['date', 'asset'])
    final_count = len(df_clean)
    
    if final_count < initial_count:
        dropped = initial_count - final_count
        warning_msg = f"Dropped {dropped} duplicate row(s) from {source_name}."
        print(f"⚠️ {warning_msg}")
        send_webhook_alert(warning_msg, "validate_data_quality")
        
    return df_clean

def load_to_database(df, table_name):
    """Loads DataFrame to PostgreSQL Cloud Database."""
    if df.empty:
        return

    db_url = os.getenv("DATABASE_URL")
    try:
        engine = create_engine(db_url)
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"✅ Data successfully pushed to table: {table_name}")
    except Exception as e:
        error_details = f"Database insertion failed for {table_name}: {e}"
        print(f"❌ {error_details}")
        send_webhook_alert(error_details, f"load_to_database ({table_name})")

if __name__ == "__main__":
    print("🚀 Starting Enterprise ETL Pipeline with Strict Data Contracts...")
    
    df_crypto = extract_crypto_data()
    df_trad = extract_traditional_markets()
    
    df_crypto_clean = validate_data_quality(df_crypto, "Crypto API")
    df_trad_clean = validate_data_quality(df_trad, "Traditional Markets API")
    
    load_to_database(df_crypto_clean, 'crypto_prices')
    load_to_database(df_trad_clean, 'traditional_markets')
    
    print("🏁 Pipeline execution completed.")