# Financial Data Engineering Pipeline - Multi-Asset Index 📈

This project is a complete Data Engineering laboratory that implements a professional ETL (Extract, Transform, Load) pipeline. It automates the collection of financial data across multiple markets, offloads complex processing to a cloud database, and provides an interactive analytics dashboard.

## 🏗️ Project Architecture

The pipeline is designed with a modern cloud-native approach, focusing on performance and resiliency:

- **Data Sources:** - Real-time Crypto extraction via CoinGecko REST API (Optimized with Batch Processing to prevent HTTP 429 errors).
  - Traditional Markets (S&P 500, Gold) extraction via Yahoo Finance API.
- **Orchestration & CI/CD:** Automated daily execution using GitHub Actions.
- **Database Layer (Supabase/PostgreSQL):** Raw data storage and advanced server-side processing using **SQL Views and Window Functions** (calculating 7-day Moving Averages and % Deltas directly in the database).
- **Application Layer:** Interactive Multi-Tab Analytics Dashboard built with Streamlit Cloud.
- **Monitoring & Alerting:** Real-time error tracking and alerting system integrated with **Discord Webhooks** to notify on API or Database failures.

## 📂 Project Structure

- `main.py`: The core ETL engine handling extraction, alerting, and database loading.
- `app.py`: Streamlit dashboard featuring multi-tab views, querying pre-processed metrics from PostgreSQL Views.
- `requirements.txt`: Project dependencies for seamless cloud deployment.
- `.github/workflows/`: Contains the YAML configuration for the automated CI/CD pipeline.

## 🛠️ Technologies Used

- **Python 3.12+**
- **Data Engineering & DB:** Pandas, SQLAlchemy, PostgreSQL (Supabase), SQL Window Functions.
- **APIs & Integration:** Requests, yfinance, Discord Webhooks.
- **Visualization:** Streamlit.
- **Infrastructure:** GitHub Actions.

## 🚀 How to Run

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/ccerks/etl-financeiro.git](https://github.com/ccerks/etl-financeiro.git)

 2. **Set up the virtual environment:**
     ```bash
     python -m venv venv
     source venv/Scripts/activate  # Windows: .\venv\Scripts\activate

3. **Install dependencies:**
     ```bash
     pip install -r requirements.txt
     
 4. **Environment Variables:**
     Create a .env file in the root directory and add:
     ```Plaintext
    DATABASE_URL=postgresql://...
    WEBHOOK_URL=[https://discord.com/api/webhooks/](https://discord.com/api/webhooks/)...

📈 Roadmap (Milestones)
[x] Multi-asset extraction and Cloud Database integration.

[x] CI/CD Automation with GitHub Actions.

[x] API Optimization (Batch Processing).

[x] Real-time Error Alerting System via Discord Webhooks.

[x] Performance Optimization migrating calculations to PostgreSQL Views.

[ ] Add Data Quality checks (Great Expectations) before database ingestion.

**Developed by** [Caio Cerqueira](https://github.com/ccerks) 🚀
