import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Financial Analytics Pro", page_icon="📈", layout="wide")

@st.cache_data(ttl=600)
def load_data(view_name):
    """Dynamically loads pre-calculated metrics from PostgreSQL Views."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        st.error("DATABASE_URL not found.")
        return pd.DataFrame()
    
    engine = create_engine(db_url)
    try:
        # Now querying the View instead of the raw table
        df = pd.read_sql_query(f"SELECT * FROM {view_name} ORDER BY date ASC", engine)
        df['date'] = pd.to_datetime(df['date'], format='mixed')
        return df
    except Exception as e:
        return pd.DataFrame()

st.title("📈 Multi-Asset Financial Dashboard")

tab1, tab2 = st.tabs(["🪙 Crypto Assets", "🏦 Traditional Markets"])

with tab1:
    # Querying the Crypto View
    df_crypto = load_data('vw_crypto_metrics')
    
    if not df_crypto.empty:
        asset = st.selectbox("Select Crypto Asset", df_crypto['asset'].unique(), key="crypto_select")
        filtered_df = df_crypto[df_crypto['asset'] == asset].copy()
        
        if len(filtered_df) > 1:
            last_record = filtered_df.iloc[-1]
            
            col1, col2, col3 = st.columns(3)
            # Directly using the delta_pct and ma7 calculated by the database
            col1.metric("Current Price", f"${last_record['price_usd']:,.2f}", f"{last_record['delta_pct']:.2f}%")
            col2.metric("7D Moving Average", f"${last_record['ma7']:,.2f}")
            col3.metric("30D High", f"${filtered_df['price_usd'].max():,.2f}")

            st.subheader(f"Price Trend vs 7-Day Average: {asset.upper()}")
            chart_data = filtered_df.set_index('date')[['price_usd', 'ma7']]
            st.line_chart(chart_data)
        else:
            st.info("Gathering more data to display trends and metrics...")
        
        with st.expander("🔍 View Pre-Processed Database Records"):
            st.dataframe(filtered_df.sort_values('date', ascending=False), use_container_width=True)
    else:
        st.info("Waiting for data or View creation in Supabase...")

with tab2:
    # Querying the Traditional View
    df_trad = load_data('vw_traditional_metrics')
    
    if not df_trad.empty:
        asset_trad = st.selectbox("Select Traditional Asset", df_trad['asset'].unique(), key="trad_select")
        filtered_trad = df_trad[df_trad['asset'] == asset_trad].copy()
        
        last_record_trad = filtered_trad.iloc[-1]
        
        # Displaying metrics securely with .get() to prevent NoneType errors on day 1
        delta_trad = last_record_trad.get('delta_pct', 0)
        delta_display = f"{delta_trad:.2f}%" if pd.notnull(delta_trad) else "0.00%"
        
        col1, col2 = st.columns(2)
        col1.metric(f"Current Price ({asset_trad})", f"${last_record_trad['price_usd']:,.2f}", delta_display)
        col2.metric("7D Moving Average", f"${last_record_trad['ma7']:,.2f}")
        
        st.subheader(f"Historical Trend: {asset_trad}")
        chart_data_trad = filtered_trad.set_index('date')[['price_usd', 'ma7']]
        st.line_chart(chart_data_trad)
        
        with st.expander("🔍 View Pre-Processed Database Records"):
            st.dataframe(filtered_trad.sort_values('date', ascending=False), use_container_width=True)
    else:
        st.info("Waiting for data or View creation in Supabase...")