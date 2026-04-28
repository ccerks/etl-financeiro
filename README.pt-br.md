# Pipeline de Engenharia de Dados Financeiros - Índice Multi-Ativos 📈
> 🇺🇸 [Read in English](README.md) | 🇧🇷 Português

Este projeto é um laboratório completo de Engenharia de Dados que implementa um pipeline ETL (Extract, Transform, Load) profissional. Ele automatiza a coleta de dados financeiros em múltiplos mercados, impõe contratos rigorosos de qualidade de dados, transfere o processamento analítico para um banco de dados em nuvem e fornece um dashboard interativo.

## 🏗️ Arquitetura do Projeto

O pipeline foi desenhado com uma abordagem *cloud-native* moderna, focando em performance, integridade de dados e resiliência:

- **Fontes de Dados (Camada Bronze):** - Extração de Criptomoedas em tempo real via API REST da CoinGecko (Otimizada com *Batch Processing* para evitar erros HTTP 429 de *Rate Limiting*).
  - Extração de Mercados Tradicionais (S&P 500, Ouro) via API do Yahoo Finance.
- **Qualidade de Dados e Contratos (Camada Silver):** Imposição de schema estrito usando **Pydantic** (tipagem a nível de linha e validação lógica) e Pandas (unicidade e completude a nível de dataset) antes de qualquer inserção no banco.
- **Camada de Banco de Dados (Camada Gold - Supabase/PostgreSQL):** - **Idempotência:** Garantida através de Chaves Primárias Compostas (Data + Ativo) para prevenir duplicidade de dados.
  - **Processamento Server-Side:** Analytics avançado usando **SQL Views e Window Functions** (calculando Médias Móveis de 7 dias e variações percentuais diretamente no banco para otimizar a performance do frontend).
- **Orquestração e CI/CD:** Execução diária automatizada usando GitHub Actions. O pipeline atua como um *gatekeeper*, rodando **Testes Unitários Automatizados (Pytest)** antes de executar o script ETL.
- **Monitoramento e Alertas:** Sistema de rastreamento de erros em tempo real integrado com **Webhooks do Discord** para notificar imediatamente sobre anomalias nas APIs, violações de schema ou falhas no banco de dados.

## 📂 Estrutura do Projeto

- `main.py`: O motor central do ETL, responsável pela extração, validação de qualidade, alertas e carga no banco.
- `test_main.py`: Testes unitários automatizados validando os contratos de dados do Pydantic.
- `app.py`: Dashboard em Streamlit com múltiplas abas, consultando as métricas pré-processadas das Views do PostgreSQL.
- `requirements.txt`: Dependências do projeto para deploy contínuo em nuvem.
- `.github/workflows/`: Contém a configuração YAML para o pipeline automatizado de CI/CD.

## 🛠️ Tecnologias Utilizadas

- **Python 3.12+**
- **Engenharia de Dados & BD:** Pandas, SQLAlchemy, PostgreSQL (Supabase), SQL Window Functions.
- **Qualidade de Dados & Testes:** Pydantic (Data Contracts), Pytest (TDD).
- **APIs & Integração:** Requests, yfinance, Discord Webhooks.
- **Visualização:** Streamlit.
- **Infraestrutura:** GitHub Actions (CI/CD).

## 🚀 Como Executar

1. **Clone o repositório**
   ```bash
   git clone [https://github.com/ccerks/etl-financeiro.git](https://github.com/ccerks/etl-financeiro.git)

 2. **Configure o ambiente virtual:**
     ```bash
     python -m venv venv
     source venv/Scripts/activate  # Windows: .\venv\Scripts\activate

3. **Instale as dependências:**
     ```bash
     pip install -r requirements.txt
     
 4. **Variáveis de Ambiente:**
     Crie um arquivo .env na raiz do projeto e adicione suas credenciais::
     ```Plaintext
    DATABASE_URL=postgresql://...
    WEBHOOK_URL=[https://discord.com/api/webhooks/](https://discord.com/api/webhooks/)...

📈 Roadmap (Milestones)
- [x] Extração multi-ativos e integração com Banco de Dados em Nuvem.

- [x] Otimização de API (Batch Processing) para lidar com limites de requisição.

- [x] Sistema de Alertas em tempo real via Webhooks do Discord.

- [x] Otimização de Performance migrando cálculos para Views do PostgreSQL.

- [x] Qualidade e Integridade de Dados: Implementação de Contratos de Dados com Pydantic e validação com Pandas.

- [x] Resiliência do Banco de Dados: Aplicação de Idempotência usando Chaves Primárias Compostas.

- [x] Automação CI/CD: Workflow automatizado no GitHub Actions com validação do Pytest.

- [ ] Atualização Futura: Migrar a granularidade do banco de dados de Diária (Date) para Intra-day (Timestamp) para suportar gráficos de candlestick de alta frequência.

**Desenvolvido por:** [Caio Cerqueira](https://github.com/ccerks) 🚀
