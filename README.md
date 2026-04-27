# Financial Data Engineering Pipeline - Multi-Asset Index 📈

This project is a complete Data Engineering laboratory that implements a professional ETL (Extract, Transform, Load) pipeline. It automates the collection of financial data across multiple markets (Cryptocurrencies and Traditional Assets), stores it in a cloud-based relational database, and provides an interactive analytics dashboard.

## 🏗️ Project Architecture

The pipeline is designed with a modern cloud-native approach and multi-source integration:

- **Data Sources:** - Real-time Crypto extraction via CoinGecko REST API (Optimized with Batch Processing to handle Rate Limiting).
  - Traditional Markets (S&P 500, Gold) extraction via Yahoo Finance API.
- **Orchestration:** Automated execution using GitHub Actions (CI/CD) running on a daily cron schedule.
- **Storage:** Cloud-based PostgreSQL database (Supabase) managed with SQLAlchemy.
- **Frontend:** Interactive Multi-Tab Analytics Dashboard built with Streamlit Cloud.
- **Security:** Strict Secret Management for Database URLs via GitHub Secrets and Streamlit Cloud configuration.

## 📂 Project Structure

- `main.py`: The core ETL engine handling extraction, transformation, and database loading.
- `app.py`: Streamlit dashboard featuring multi-tab views, moving averages (MA7), and percentage deltas.
- `notebooks/`: Experimental development, data modeling, and API testing.
- `requirements.txt`: Project dependencies for seamless cloud deployment.
- `.github/workflows/`: Contains the YAML configuration for the automated CI/CD pipeline.

## 🛠️ Technologies Used

- **Python 3.12+**
- **Data Engineering:** Pandas, SQLAlchemy, psycopg2-binary.
- **APIs & Extraction:** Requests, yfinance.
- **Visualization:** Streamlit.
- **Infrastructure:** PostgreSQL (Supabase), GitHub Actions.

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
     ```bash
     Create a .env file and add your DATABASE_URL.

📈 Roadmap (Milestones)
[x] Multi-asset extraction implementation.

[x] Cloud Database migration (SQLite to PostgreSQL/Supabase).

[x] CI/CD Automation with GitHub Actions.

[x] Interactive Dashboard with Moving Averages and KPIs.

[x] Multi-Source Integration (Crypto + Traditional Markets).

[x] API Optimization (Batch Processing to prevent HTTP 429 errors).

[ ] Implement robust Logging & Error Handling system.

**Developed by** [Caio Cerqueira](https://github.com/ccerks) 🚀
