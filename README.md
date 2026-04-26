# Financial Data Engineering Pipeline - Crypto Index 📈

This project is a complete Data Engineering laboratory that implements a professional ETL (Extract, Transform, Load) pipeline. It automates the collection of cryptocurrency data, stores it in a cloud-based relational database, and provides an interactive analytics dashboard.

## 🏗️ Project Architecture

The pipeline is designed with a modern cloud-native approach:

- **Data Source:** Real-time data extraction via CoinGecko REST API.
- **Orchestration:** Automated execution using GitHub Actions (CI/CD).
- **Storage:** Cloud-based PostgreSQL database (Supabase) using SQLAlchemy.
- **Frontend:** Interactive Analytics Dashboard built with Streamlit Cloud.
- **Security:** Environment variable management (`.env`) and Secret Management (GitHub/Streamlit).

## 📂 Project Structure

- `main.py`: The core ETL engine (Extraction & Cloud Loading).
- `app.py`: Streamlit dashboard with financial indicators (MA7, % Delta).
- `notebooks/`: Experimental development and API testing.
- `requirements.txt`: Project dependencies for cloud deployment.
- `.env`: Local credentials (ignored by Git).

## 🛠️ Technologies Used

- **Python 3.12+**
- **Pandas:** Data manipulation and feature engineering.
- **SQLAlchemy:** SQL Toolkit and Object Relational Mapper (ORM).
- **Streamlit:** Interactive data visualization.
- **PostgreSQL (Supabase):** Relational cloud database.
- **GitHub Actions:** Automated workflow orchestration.

## 🚀 How to Run

  1. **Clone the repository:**
     ```bash
     git clone https://github.com/ccerks/etl-financeiro.git
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

[ ] Implement Logging & Error Handling system.

**Developed by** [Caio Cerqueira](https://github.com/ccerks) 🚀
