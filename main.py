import pandas as pd
import requests
import os
import yfinance as yf
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def extract_crypto_data():
    """Extracts cryptocurrency data from CoinGecko API using a single batch request."""
    assets = ['bitcoin', 'ethereum', 'solana', 'cardano']
    
    # Convert list to comma-separated string: "bitcoin,ethereum,solana,cardano"
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
            else:
                print(f"⚠️ Warning: {asset} not found in API response.")
                
    except Exception as e:
        print(f"❌ Error fetching crypto data: {e}")
            
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
            print(f"Error fetching {name}: {e}")

    return pd.DataFrame(data_list)

def load_to_database(df, table_name):
    """Loads DataFrame to PostgreSQL Cloud Database."""
    if df.empty:
        print(f"⚠️ No data to load for {table_name}.")
        return

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not found in environment variables.")
    
    engine = create_engine(db_url)
    df.to_sql(table_name, engine, if_exists='append', index=False)
    print(f"✅ Data successfully pushed to table: {table_name}")

if __name__ == "__main__":
    print("🚀 Starting Multi-Source ETL Pipeline...")
    
    # 1. Extraction
    df_crypto = extract_crypto_data()
    df_traditional = extract_traditional_markets()
    
    # 2. Load
    load_to_database(df_crypto, 'crypto_prices')
    load_to_database(df_traditional, 'traditional_markets')
    
    print("🏁 Pipeline execution completed.")