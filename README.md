# Financial Data Extraction Pipeline - Crypto Index 📈

This project is a Data Engineering laboratory focused on building an ETL (Extract, Transform, Load) pipeline for monitoring financial assets. Currently, the pipeline extracts historical cryptocurrency data via API and processes the information for further analysis.

## 🏗️ Project Architecture

The project follows an organized structure to ensure scalability and security:

- `notebooks/`: Contains Jupyter Notebooks used for experimentation and development of the extraction code.
- `data/`: Local directory for storing processed files (CSV/Parquet). *Note: data files are ignored by Git following storage best practices.*
- `.env`: Management of credentials and API keys (protected for security).
- `.gitignore`: Configuration to prevent uploading virtual environments, sensitive data, and temporary files.

## 🛠️ Technologies Used

- **Language:** Python 3.12+
- **Libraries:** - `Pandas`: For data manipulation and cleaning.
  - `Requests`: For consuming the CoinGecko API.
  - `Python-dotenv`: For environment variable management.
- **Environment:** VS Code with Jupyter extensions.
- **Version Control:** Git & GitHub.

## 🚀 How to Run

  1. **Clone the repository:**
     ```bash
     git clone https://github.com/ccerks/etl-financeiro.git
  2. **Set up the virtual environment:**
     ```bash
     python -m venv venv
     source venv/Scripts/activate  # On Windows
  3. **Install dependencies:**
     ```bash
     pip install pandas requests python-dotenv ipykernel
  
  4. **Environment Variables:**
      Create a .env file in the root directory and add your keys (if necessary).

📈 Roadmap

   [x] Initial Bitcoin data extraction.
    
   [x] Professional versioning and folder structure.
    
   [x] Multi-asset extraction implementation (Loops and Functions).
    
   [x] Data persistence in SQLite/PostgreSQL database.
    
   [ ] Pipeline orchestration for automated execution.

**Developed by** [Caio Cerqueira](https://github.com/ccerks) 🚀
