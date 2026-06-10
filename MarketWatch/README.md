# 📈 MarketWatch — Equity Risk Analytics

> An end-to-end Python pipeline that ingests market data, persists it to SQL, computes portfolio risk metrics (Value-at-Risk & volatility), and serves them through an interactive dashboard.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-dashboard-red?logo=streamlit)
![SQLite](https://img.shields.io/badge/SQLite-database-green?logo=sqlite)
![Tests](https://img.shields.io/badge/tests-pytest-orange)

## 🎥 Demo

<img width="1870" height="872" alt="Demo" src="https://github.com/user-attachments/assets/00002705-ec8e-4744-a388-63d30a5be385" />




## 🎯 Overview

MarketWatch demonstrates a complete data analytics workflow that mirrors how risk and analytics teams operate in practice:

**Fetch → Clean → Store in SQL → Query → Analyze → Visualize**

The project computes key risk metrics commonly used in portfolio and trading analytics:

- **Historical Value-at-Risk (VaR)** — loss threshold on the worst X% of trading days
- **Conditional VaR (CVaR / Expected Shortfall)** — average loss beyond the VaR threshold
- **Annualized Rolling Volatility** — risk measured over a configurable time window

---

## ✨ Key Features

| Feature | Description |
|----------|-------------|
| 📥 Data Ingestion | Pulls historical price data from Yahoo Finance |
| 🗄️ SQL Persistence | Stores cleaned market data in SQLite |
| 📊 Risk Modeling | Calculates Historical VaR and CVaR at configurable confidence levels |
| 📈 Volatility Analysis | Computes rolling annualized volatility using log returns |
| 🖥️ Interactive Dashboard | Streamlit dashboard with configurable tickers and parameters |
| ✅ Unit Tested | Financial calculations validated with pytest |

---

## 🛠️ Tech Stack

**Language**
- Python 3.10+

**Data & Analytics**
- pandas
- NumPy
- yfinance

**Database**
- SQLite (`sqlite3`)

**Visualization**
- Streamlit
- Matplotlib

**Testing**
- pytest

---

## 🏗️ Architecture

```text
Yahoo Finance
      │
      ▼
 ingestion.py
      │
      ▼
 cleaner.py
      │
      ▼
 database.py (SQLite)
      │
 ┌────┴────┐
 ▼         ▼
risk.py  volatility.py
      │
      ▼
dashboard.py
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+

### Installation

```bash
git clone https://github.com/<your-username>/MarketWatch.git
cd MarketWatch

python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

### Run the Dashboard

```bash
streamlit run dashboard.py
```

### Run the Pipeline

```bash
python main.py
```

### Run Ad-hoc SQL Analysis

```bash
python analysis.py
```

---

## 🧪 Testing

Run all tests:

```bash
pytest -v
```

### Test Coverage

- VaR calculations
- CVaR calculations
- Confidence-level sensitivity
- Volatility calculations
- Per-ticker volatility independence
- Dollar VaR scaling with position size

---

## 📂 Project Structure

```text
MarketWatch/
├── dashboard.py
├── main.py
├── ingestion.py
├── cleaner.py
├── database.py
├── volatility.py
├── risk.py
├── analysis.py
├── plotter.py
├── requirements.txt
├── Demo.gif
│
└── tests/
    ├── test_risk.py
    └── test_volatility.py
```

---

## 📜 License

This project is intended for educational and portfolio purposes.
