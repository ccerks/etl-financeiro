import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Financial Analytics Pro", page_icon="📈", layout="wide")

@st.cache_data(ttl=600)
def load_data(table_name):
    """Dynamically loads data from specified database table."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        st.error("DATABASE_URL not found.")
        return pd.DataFrame()
    
    engine = create_engine(db_url)
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name} ORDER BY date ASC", engine)
        df['date'] = pd.to_datetime(df['date'], format='mixed')
        return df
    except Exception as e:
        return pd.DataFrame()

st.title("📈 Multi-Asset Financial Dashboard")

# Creating Tabs for different market sectors
tab1, tab2 = st.tabs(["🪙 Crypto Assets", "🏦 Traditional Markets"])

with tab1:
    df_crypto = load_data('crypto_prices')
    
    if not df_crypto.empty:
        asset = st.selectbox("Select Crypto Asset", df_crypto['asset'].unique(), key="crypto_select")
        filtered_df = df_crypto[df_crypto['asset'] == asset].copy()
        
        if len(filtered_df) > 1:
            filtered_df['MA7'] = filtered_df['price_usd'].rolling(window=7).mean()
            last_price = filtered_df['price_usd'].iloc[-1]
            prev_price = filtered_df['price_usd'].iloc[-2]
            delta_pct = ((last_price - prev_price) / prev_price) * 100
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Current Price", f"${last_price:,.2f}", f"{delta_pct:.2f}%")
            col2.metric("7D Moving Average", f"${filtered_df['MA7'].iloc[-1]:,.2f}")
            col3.metric("30D High", f"${filtered_df['price_usd'].max():,.2f}")

            st.subheader(f"Price Trend vs 7-Day Average: {asset.upper()}")
            chart_data = filtered_df.set_index('date')[['price_usd', 'MA7']]
            st.line_chart(chart_data)
        else:
            st.info("Gathering more data to display trends and metrics...")
        
        with st.expander("🔍 View Raw Crypto Data"):
            st.dataframe(filtered_df.sort_values('date', ascending=False), use_container_width=True)
    else:
        st.info("Waiting for crypto data from Supabase...")

with tab2:
    df_trad = load_data('traditional_markets')
    
    if not df_trad.empty:
        asset_trad = st.selectbox("Select Traditional Asset", df_trad['asset'].unique(), key="trad_select")
        filtered_trad = df_trad[df_trad['asset'] == asset_trad].copy()
        
        last_price_trad = filtered_trad['price_usd'].iloc[-1]
        st.metric(f"Current Price ({asset_trad})", f"${last_price_trad:,.2f}")
        
        # Line chart will look like a dot until we have 2 days of data
        st.subheader(f"Historical Trend: {asset_trad}")
        st.line_chart(filtered_trad.set_index('date')[['price_usd']])
        
        with st.expander("🔍 View Raw Traditional Data"):
            st.dataframe(filtered_trad.sort_values('date', ascending=False), use_container_width=True)
    else:
        st.info("Waiting for traditional market data from Supabase...")