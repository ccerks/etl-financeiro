import requests
import pandas as pd
import time
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carrega as senhas do arquivo .env
load_dotenv()

def fetch_crypto_data(asset_list):
    """Fetches market data from CoinGecko API."""
    all_frames = []
    for asset in asset_list:
        url = f"https://api.coingecko.com/api/v3/coins/{asset}/market_chart?vs_currency=usd&days=30"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            df_temp = pd.DataFrame(data['prices'], columns=['timestamp', 'price_usd'])
            df_temp['asset'] = asset
            df_temp['date'] = pd.to_datetime(df_temp['timestamp'], unit='ms')
            all_frames.append(df_temp[['date', 'asset', 'price_usd']])
            time.sleep(1.5)
        else:
            print(f"⚠️ Warning: Could not fetch {asset}. Status: {response.status_code}")
            
    if not all_frames:
        return pd.DataFrame()

    combined_df = pd.concat(all_frames, ignore_index=True)
    return combined_df.sort_values(by=['date', 'asset']).reset_index(drop=True)

def save_to_supabase(df):
    """Persists the DataFrame into the Supabase (PostgreSQL) database."""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ Error: DATABASE_URL not found in environment variables.")
        return

    try:
        engine = create_engine(database_url)
        df.to_sql('crypto_prices', engine, if_exists='append', index=False)
        print("✅ Data successfully pushed to Supabase Cloud!")
    except Exception as e:
        print(f"❌ Cloud Database error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Cloud-Native ETL Pipeline...")
    assets = ['bitcoin', 'ethereum', 'solana', 'cardano']
    data = fetch_crypto_data(assets)
    
    if not data.empty:
        save_to_supabase(data)