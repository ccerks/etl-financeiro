import requests
import pandas as pd
import sqlite3
import time
import os

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

def save_to_database(df, db_path='data/finance_data.db'):
    """Saves DataFrame to SQLite database."""
    # Ensure the directory exists before saving
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    try:
        conn = sqlite3.connect(db_path)
        df.to_sql('crypto_prices', conn, if_exists='append', index=False)
        conn.close()
        print(f"✅ Data successfully persisted in {db_path}")
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Automated ETL Pipeline...")
    my_assets = ['bitcoin', 'ethereum', 'solana', 'cardano']
    
    # 1. Extract & Transform
    final_data = fetch_crypto_data(my_assets)
    
    # 2. Load
    if not final_data.empty:
        save_to_database(final_data)
        print("🎉 ETL Run Completed Successfully!")
    else:
        print("❌ ETL Run Failed: No data extracted.")