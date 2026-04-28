# Financial Data Engineering Pipeline - Multi-Asset Index 📈
> 🇺🇸 English | 🇧🇷 [Ver versão em Português](README.pt-br.md)

This project is a complete Data Engineering laboratory that implements a professional ETL (Extract, Transform, Load) pipeline. It automates the collection of financial data across multiple markets, enforces strict data quality contracts, offloads complex processing to a cloud database, and provides an interactive analytics dashboard.

## 🏗️ Project Architecture

The pipeline is designed with a modern cloud-native approach, focusing on performance, data integrity, and resiliency:

- **Data Sources (Bronze Layer):** - Real-time Crypto extraction via CoinGecko REST API (Optimized with Batch Processing to prevent HTTP 429 Rate Limiting errors).
  - Traditional Markets (S&P 500, Gold) extraction via Yahoo Finance API.
- **Data Quality & Contracts (Silver Layer):** Strict schema enforcement using **Pydantic** (row-level typing and logical validation) and Pandas (dataset-level uniqueness and completeness) before any database insertion.
- **Database Layer (Gold Layer - Supabase/PostgreSQL):** - **Idempotency:** Enforced via Composite Primary Keys (Date + Asset) to prevent data duplication.
  - **Server-Side Processing:** Advanced analytics using **SQL Views and Window Functions** (calculating 7-day Moving Averages and % Deltas directly in the database to optimize frontend performance).
- **Orchestration & CI/CD:** Automated daily execution using GitHub Actions. The pipeline acts as a gatekeeper, running **Automated Unit Tests (Pytest)** before executing the ETL script.
- **Monitoring & Alerting:** Real-time error tracking system integrated with **Discord Webhooks** to notify immediately on API anomalies, schema violations, or database failures.

## 📂 Project Structure

- `main.py`: The core ETL engine handling extraction, data quality validation, alerting, and database loading.
- `test_main.py`: Automated unit tests validating Pydantic data contracts.
- `app.py`: Streamlit dashboard featuring multi-tab views, querying pre-processed metrics from PostgreSQL Views.
- `requirements.txt`: Project dependencies for seamless cloud deployment.
- `.github/workflows/`: Contains the YAML configuration for the automated CI/CD pipeline.

## 🛠️ Technologies Used

- **Python 3.12+**
- **Data Engineering & DB:** Pandas, SQLAlchemy, PostgreSQL (Supabase), SQL Window Functions.
- **Data Quality & Testing:** Pydantic (Data Contracts), Pytest (TDD).
- **APIs & Integration:** Requests, yfinance, Discord Webhooks.
- **Visualization:** Streamlit.
- **Infrastructure:** GitHub Actions (CI/CD).

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
- [x] Multi-asset extraction and Cloud Database integration.

- [x] API Optimization (Batch Processing) for Rate Limit handling.

- [x] Real-time Error Alerting System via Discord Webhooks.

- [x] Performance Optimization migrating calculations to PostgreSQL Views.

- [x] Data Quality & Integrity: Implemented Pydantic Data Contracts and Pandas validation.

- [x] Database Resiliency: Enforced Idempotency using Composite Primary Keys.

- [x] CI/CD Automation: Automated GitHub Actions workflow with Pytest gatekeeping.

- [ ] Future Upgrade: Migrate database granularity from Daily (Date) to Intra-day (Timestamp) to support high-frequency candlestick charting.

**Developed by** [Caio Cerqueira](https://github.com/ccerks) 🚀
