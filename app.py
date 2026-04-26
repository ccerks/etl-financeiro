import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Crypto Analytics Pro", page_icon="📊", layout="wide")

@st.cache_data(ttl=600) # Cache de 10 minutos para economizar chamadas ao banco
def load_data():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        st.error("DATABASE_URL not found.")
        return pd.DataFrame()
    
    engine = create_engine(db_url)
    df = pd.read_sql_query("SELECT * FROM crypto_prices ORDER BY date ASC", engine)
    df['date'] = pd.to_datetime(df['date'], format='mixed')
    return df

st.title("📊 Crypto Analytics Dashboard")

df = load_data()

if not df.empty:
    # Sidebar
    asset = st.sidebar.selectbox("Select Asset", df['asset'].unique())
    
    # Data Processing
    filtered_df = df[df['asset'] == asset].copy()
    
    # Feature Engineering
    filtered_df['MA7'] = filtered_df['price_usd'].rolling(window=7).mean()
    
    # Metrics Calculation
    last_price = filtered_df['price_usd'].iloc[-1]
    prev_price = filtered_df['price_usd'].iloc[-2]
    delta_pct = ((last_price - prev_price) / prev_price) * 100
    
    # Display Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"${last_price:,.2f}", f"{delta_pct:.2f}%")
    col2.metric("7D Moving Average", f"${filtered_df['MA7'].iloc[-1]:,.2f}")
    col3.metric("30D High", f"${filtered_df['price_usd'].max():,.2f}")

    # Advanced Charting
    st.subheader(f"Price Trend vs 7-Day Average: {asset.upper()}")
    # Plotting multiple lines
    chart_data = filtered_df.set_index('date')[['price_usd', 'MA7']]
    st.line_chart(chart_data)

    with st.expander("🔍 Inspection Area"):
        st.dataframe(filtered_df.sort_values('date', ascending=False), use_container_width=True)
else:
    st.info("Waiting for data from Supabase...")