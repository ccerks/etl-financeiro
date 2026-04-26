# Pipeline de Extração de Dados Financeiros - Crypto Index 📈

Este projeto é um laboratório de Engenharia de Dados focado na construção de um pipeline ETL (Extract, Transform, Load) para monitoramento de ativos financeiros. Atualmente, o pipeline realiza a extração de dados históricos de criptoativos via API e processa as informações para análise.

## 🏗️ Arquitetura do Projeto

O projeto segue uma estrutura organizada para garantir a escalabilidade e segurança:

- `notebooks/`: Contém os Jupyter Notebooks utilizados para experimentação e desenvolvimento do código de extração.
- `data/`: Diretório local destinado ao armazenamento dos arquivos processados (CSV/Parquet). *Nota: os arquivos de dados são ignorados pelo Git para seguir as boas práticas de storage.*
- `.env`: Gerenciamento de credenciais e chaves de API (protegido por segurança).
- `.gitignore`: Configuração para impedir o upload de ambientes virtuais, dados sensíveis e arquivos temporários.

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.12+
- **Bibliotecas:** - `Pandas`: Para manipulação e limpeza de dados.
  - `Requests`: Para consumo da API CoinGecko.
  - `Python-dotenv`: Para gerenciamento de variáveis de ambiente.
- **Ambiente:** VS Code com extensões Jupyter.
- **Versionamento:** Git & GitHub.

## 🚀 Como Executar

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/ccerks/etl-financeiro.git](https://github.com/ccerks/etl-financeiro.git)
  
2. **Configure o ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # No Windows

3. **Configure o ambiente virtual:**
   ```bash
   pip install pandas requests python-dotenv ipykernel
