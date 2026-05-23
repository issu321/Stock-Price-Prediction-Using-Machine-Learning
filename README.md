<div align="center">

# 📈 NeuralTrade AI

### *Stock Price Prediction Using Machine Learning*

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python&logoColor=white&color=00f0ff)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white&color=a78bfa)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3%2B-orange?style=for-the-badge&logo=scikit-learn&logoColor=white&color=34d399)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&color=fbbf24)](LICENSE)

**A next-generation, AI-powered stock price prediction platform**

[🚀 Live Demo](#) • [📖 Documentation](#installation) • [🤖 ML Models](#machine-learning-explanation) • [📊 Analytics](#stock-analytics-explanation)

<img src="https://img.shields.io/badge/Developed%20by-issu321-00f0ff?style=for-the-badge&logo=github&logoColor=white" alt="Developer">

</div>

---

## 🌟 Introduction

Welcome to **NeuralTrade AI** — a production-quality, futuristic stock price prediction system that harnesses the power of **machine learning** to analyze historical market data, compare predictive models, and forecast future stock prices with professional-grade visualizations.

Built with **Python 3.11+**, **Streamlit**, and **scikit-learn**, this project delivers an immersive cyberpunk-themed dashboard experience designed for:
- 📊 **Financial analysts** exploring ML-driven insights
- 🎓 **Students & interns** learning real-world ML pipelines
- 💼 **Portfolio builders** showcasing end-to-end ML projects
- 🔬 **Researchers** experimenting with stock prediction algorithms

> ⚡ **Key Highlight:** Train and compare 4 ML models (Linear Regression, Random Forest, Decision Tree, SVR) in real-time with live stock data from Yahoo Finance.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔮 **Real-time Predictions** | Fetch live stock data via yFinance and predict next-day prices |
| 🤖 **4 ML Models** | Linear Regression, Random Forest, Decision Tree, Support Vector Regressor |
| 📊 **Interactive Charts** | Candlestick, volume, moving averages, Bollinger Bands, RSI, MACD |
| 🏆 **Model Comparison** | Side-by-side R², MAE, RMSE, MAPE metrics with winner selection |
| 📅 **Future Forecasting** | Multi-day price forecasts with recursive prediction engine |
| 🧠 **AI Explanation Engine** | Auto-generated readable market analysis and trend summaries |
| 📁 **CSV Upload Support** | Analyze your own custom datasets |
| 💾 **Model Persistence** | Save and load best models with joblib |
| 🎨 **Cyberpunk UI** | Dark futuristic theme with neon accents and glowing effects |
| 📥 **Download Reports** | Export predictions and data as CSV files |

---

## 🖼️ Screenshots

> *Screenshots are placeholder representations of the actual UI.*

```
┌─────────────────────────────────────────────────────────────┐
│  📈 NeuralTrade AI                                          │
│  Advanced Machine Learning Stock Price Prediction System    │
├─────────────────────────────────────────────────────────────┤
│  [🏠 Home] [📊 Analysis] [🤖 ML] [📉 Compare] [🔮 Forecast] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│   │ $153.75  │  │ +2.34%   │  │ 45.2M    │  │ $155.50  │   │
│   │ Current  │  │ Change   │  │ Volume   │  │ High     │   │
│   └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │         [Candlestick Chart with MAs]                │   │
│   │                                                     │   │
│   │    📈 Green candles rising...                       │   │
│   │    📉 Red candles falling...                        │   │
│   │    MA20 ──────────────── MA50 ────────────────      │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
│   🏆 Best Model: Random Forest (R² = 0.9472)               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Installation

### Prerequisites
- Python **3.11** or higher
- pip package manager
- Internet connection (for yFinance data fetching)

### Quick Start

#### Linux / macOS
```bash
# Clone the repository
git clone https://github.com/issu321/Stock-Price-Prediction-Using-Machine-Learning.git
cd Stock-Price-Prediction-Using-Machine-Learning

# Run the installer
chmod +x install.sh
./install.sh
```

#### Windows
```powershell
# Clone the repository
git clone https://github.com/issu321/Stock-Price-Prediction-Using-Machine-Learning.git
cd Stock-Price-Prediction-Using-Machine-Learning

# Run the installer
install.bat
```

#### Manual Installation
```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## 📖 Usage Instructions

### 1. Fetch Stock Data
- Enter a stock ticker (e.g., `AAPL`, `TSLA`, `GOOGL`) in the sidebar
- Select historical period (1mo, 3mo, 6mo, 1y, 2y, 5y)
- Navigate to **Stock Analysis** to visualize trends

### 2. Train ML Models
- Go to **ML Predictions**
- The app automatically trains all 4 models
- View the best model, metrics, and AI-generated analysis

### 3. Compare Models
- Visit **Model Comparison** for side-by-side evaluation
- See R², MAE, RMSE, and MAPE for each algorithm
- View Random Forest feature importances

### 4. Forecast Future Prices
- Go to **Future Forecast**
- Adjust forecast horizon (1-30 days)
- View predicted trajectory and download CSV

### 5. Upload Custom Data
- Navigate to **CSV Upload**
- Upload your own dataset with `Date` and `Close` columns
- Analyze private or unlisted stocks

---

## 🤖 Machine Learning Explanation

### Models Implemented

| Model | Type | Strengths |
|-------|------|-----------|
| **Linear Regression** | Parametric | Fast, interpretable baseline |
| **Random Forest** | Ensemble | Robust, handles non-linearity, feature importance |
| **Decision Tree** | Tree-based | Interpretable rules, no scaling needed |
| **Support Vector Regressor** | Kernel-based | Effective in high-dimensional spaces |

### Feature Engineering Pipeline

The system extracts **30+ engineered features** from raw OHLCV data:

- **Price Features:** Daily returns, price range, price change
- **Moving Averages:** MA/EMA (5, 10, 20, 50 days)
- **Volatility:** 5-day and 20-day rolling standard deviation
- **Lag Features:** Close and volume lags (1, 2, 3, 5 days)
- **Technical Indicators:**
  - **RSI** (Relative Strength Index) — momentum oscillator
  - **MACD** — trend-following momentum indicator
  - **Bollinger Bands** — volatility envelope

### Evaluation Metrics

| Metric | Formula | Purpose |
|--------|---------|---------|
| **R² Score** | 1 - (SS_res / SS_tot) | Variance explained (1.0 = perfect) |
| **MAE** | mean(\|y - ŷ\|) | Average absolute error in dollars |
| **RMSE** | sqrt(mean((y - ŷ)²)) | Penalizes large errors |
| **MAPE** | mean(\|y - ŷ\| / y) × 100 | Percentage error |

### Auto-Model Selection
The system automatically selects the **best-performing model** based on the highest R² score and persists it using `joblib` for future forecasting.

---

## 📊 Stock Analytics Explanation

### Visualizations

| Chart | What It Shows |
|-------|---------------|
| **Candlestick** | Open, High, Low, Close prices with trend |
| **Volume** | Trading activity intensity |
| **Daily Returns** | Day-to-day percentage changes |
| **Moving Averages** | Smoothed price trends (MA20, MA50) |
| **Bollinger Bands** | Price volatility envelope |
| **RSI** | Overbought (>70) / Oversold (<30) signals |
| **MACD** | Trend momentum and crossover signals |

### Financial Metrics

| Metric | Interpretation |
|--------|----------------|
| **Volatility** | Risk measure; higher = more unpredictable |
| **Period High/Low** | Price extremes in selected timeframe |
| **Growth Trend** | Direction based on moving average comparison |
| **Momentum** | RSI-based speed and strength of price movement |

---

## 📁 Folder Structure

```
Stock-Price-Prediction-Using-Machine-Learning/
│
├── app.py                  # Main Streamlit application (backend + frontend)
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation (this file)
├── install.sh              # Linux/macOS installer script
├── install.bat             # Windows installer script
├── inputguide.md           # Detailed user input guide
├── stock_dataset.csv       # Sample stock market dataset
├── .gitignore              # Git ignore rules
│
└── assets/
    └── styles.css          # Custom cyberpunk theme stylesheet
```

> **Design Philosophy:** The project is intentionally lightweight with minimal files. All core logic lives in `app.py` for simplicity and clarity.

---

## 🛠️ Technologies Used

<div align="center">

| Technology | Purpose | Version |
|------------|---------|---------|
| ![Python](https://img.shields.io/badge/Python-3.11+-00f0ff?style=flat&logo=python) | Core language | 3.11+ |
| ![Streamlit](https://img.shields.io/badge/Streamlit-UI-a78bfa?style=flat&logo=streamlit) | Web interface | 1.30+ |
| ![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-34d399?style=flat&logo=scikit-learn) | Machine learning | 1.3+ |
| ![yFinance](https://img.shields.io/badge/yFinance-Data-f87171?style=flat) | Stock data API | 0.2.28+ |
| ![Pandas](https://img.shields.io/badge/Pandas-Data-fbbf24?style=flat&logo=pandas) | Data processing | 2.0+ |
| ![NumPy](https://img.shields.io/badge/NumPy-Compute-00f0ff?style=flat&logo=numpy) | Numerical ops | 1.24+ |
| ![Plotly](https://img.shields.io/badge/Plotly-Charts-a78bfa?style=flat&logo=plotly) | Interactive viz | 5.15+ |
| ![Matplotlib](https://img.shields.io/badge/Matplotlib-Viz-34d399?style=flat) | Static plots | 3.7+ |
| ![joblib](https://img.shields.io/badge/joblib-Serialize-f87171?style=flat) | Model persistence | 1.3+ |

</div>

---

## 🗺️ Future Roadmap

- [ ] **LSTM/GRU Neural Networks** — Deep learning price forecasting
- [ ] **Sentiment Analysis** — Integrate news/twitter sentiment
- [ ] **Portfolio Optimization** — Multi-stock correlation analysis
- [ ] **Real-time Streaming** — WebSocket live price updates
- [ ] **Backtesting Engine** — Strategy simulation and evaluation
- [ ] **API Endpoint** — REST API for programmatic access
- [ ] **Docker Support** — Containerized deployment
- [ ] **Cloud Deployment** — Heroku / AWS / GCP ready configs

---

## 🤝 Contribution Guide

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR_USERNAME/Stock-Price-Prediction-Using-Machine-Learning.git`
3. **Create a branch**: `git checkout -b feature/amazing-feature`
4. **Make changes** and test locally
5. **Commit**: `git commit -m "Add amazing feature"`
6. **Push**: `git push origin feature/amazing-feature`
7. **Open a Pull Request** on GitHub

### Code Standards
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include type hints where appropriate
- Test with multiple stock tickers before submitting

---

## ⚠️ Disclaimer

> **This application is for educational and research purposes only.**
>
> Stock predictions generated by machine learning models are **not guaranteed to be accurate** and should **not** be used as the sole basis for investment decisions. Financial markets are influenced by countless unpredictable factors including news, geopolitical events, and market sentiment that cannot be fully captured by historical price data alone.
>
> **Always consult a qualified financial advisor** before making investment decisions. Past performance does not indicate future results. The developer assumes no liability for any financial losses incurred from using this software.

---

## 📜 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 issu321

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<div align="center">

## 👤 Developer

**[issu321](https://github.com/issu321)**

[![GitHub](https://img.shields.io/badge/GitHub-issu321-00f0ff?style=for-the-badge&logo=github)](https://github.com/issu321)
[![Repository](https://img.shields.io/badge/Repository-Stock--Price--Prediction-a78bfa?style=for-the-badge&logo=github)](https://github.com/issu321/Stock-Price-Prediction-Using-Machine-Learning)

---

*⭐ Star this repository if you find it useful!*

*Built with 💙 and Python*

</div>
