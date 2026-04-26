import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carrega as senhas do arquivo .env
load_dotenv()

# 1. Page Configuration
st.set_page_config(page_title="Crypto Index Dashboard", page_icon="📈", layout="wide")

st.title("📈 Crypto Index ETL Dashboard")
st.markdown("Interactive visualization of the Automated ETL Pipeline.")

# 2. Data Extraction Function (Cloud PostgreSQL)
@st.cache_data
def load_data():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        st.error("DATABASE_URL variable is missing.")
        return pd.DataFrame()
        
    engine = create_engine(db_url)
    df = pd.read_sql_query("SELECT * FROM crypto_prices", engine)
    
    df['date'] = pd.to_datetime(df['date'], format='mixed')
    return df

# 3. Dashboard Logic
df = load_data()

if df.empty:
    st.warning("⚠️ No data found. Please run the ETL pipeline (`main.py`) first.")
else:
    # Sidebar Filters
    st.sidebar.header("Filters")
    available_assets = df['asset'].unique()
    selected_asset = st.sidebar.selectbox("Select Cryptocurrency", available_assets)
    
    # Filter Data
    filtered_df = df[df['asset'] == selected_asset]
    
    # Key Metrics (KPIs)
    current_price = filtered_df['price_usd'].iloc[-1]
    max_price = filtered_df['price_usd'].max()
    min_price = filtered_df['price_usd'].min()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price (Last Record)", f"${current_price:.2f}")
    col2.metric("30-Day High", f"${max_price:.2f}")
    col3.metric("30-Day Low", f"${min_price:.2f}")
    
    # Line Chart
    st.subheader(f"Price History: {selected_asset.capitalize()}")
    st.line_chart(data=filtered_df, x='date', y='price_usd', use_container_width=True)
    
    # Raw Data Expander
    with st.expander("🔍 View Raw Data"):
        st.dataframe(filtered_df.sort_values(by='date', ascending=False))