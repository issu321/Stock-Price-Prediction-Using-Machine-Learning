# 📖 NeuralTrade AI - Input Guide

> **Developed by [issu321](https://github.com/issu321)**
> 
> Repository: [Stock-Price-Prediction-Using-Machine-Learning](https://github.com/issu321/Stock-Price-Prediction-Using-Machine-Learning)

---

## 📌 Table of Contents

1. [Stock Symbol Examples](#stock-symbol-examples)
2. [Prediction Examples](#prediction-examples)
3. [CSV Upload Examples](#csv-upload-examples)
4. [Dashboard Usage](#dashboard-usage)
5. [Analytics Explanation](#analytics-explanation)
6. [Troubleshooting](#troubleshooting)

---

## 📈 Stock Symbol Examples

Enter any valid stock ticker symbol in the sidebar input field. Here are popular examples:

| Symbol | Company | Sector |
|--------|---------|--------|
| AAPL | Apple Inc. | Technology |
| MSFT | Microsoft Corp. | Technology |
| GOOGL | Alphabet Inc. | Technology |
| AMZN | Amazon.com | Consumer |
| TSLA | Tesla Inc. | Automotive |
| NVDA | NVIDIA Corp. | Technology |
| META | Meta Platforms | Technology |
| NFLX | Netflix Inc. | Entertainment |
| AMD | AMD Inc. | Technology |
| INTC | Intel Corp. | Technology |
| JPM | JPMorgan Chase | Finance |
| BAC | Bank of America | Finance |
| DIS | Walt Disney | Entertainment |
| BA | Boeing Co. | Aerospace |
| XOM | Exxon Mobil | Energy |

### International Tickers
- **India**: RELIANCE.NS, TCS.NS, INFY.NS
- **UK**: SHEL.L, BP.L, ULVR.L
- **Japan**: 7203.T (Toyota), 6758.T (Sony)
- **Crypto**: BTC-USD, ETH-USD

---

## 🔮 Prediction Examples

### Example 1: Short-term Prediction (AAPL)
1. Enter `AAPL` in the ticker field
2. Select period `1y`
3. Go to **ML Predictions** page
4. Wait for model training
5. View predicted vs actual prices
6. Check AI-generated market analysis

### Example 2: Multi-day Forecast (TSLA)
1. Enter `TSLA` in the ticker field
2. Select period `2y`
3. Navigate to **Future Forecast**
4. Set forecast horizon to `14` days
5. View predicted price trajectory
6. Download forecast CSV

### Example 3: Model Comparison (NVDA)
1. Enter `NVDA` in the ticker field
2. Select period `1y`
3. Go to **Model Comparison**
4. Compare R², MAE, RMSE across all 4 models
5. View feature importance from Random Forest

---

## 📁 CSV Upload Examples

### Format Requirements

Your CSV file **must** contain at minimum:
- `Date` column (YYYY-MM-DD format)
- `Close` column (closing price)

**Optional columns** (enhance analysis):
- `Open`, `High`, `Low`, `Volume`

### Sample CSV Content

```csv
Date,Open,High,Low,Close,Volume
2023-01-03,150.10,155.50,148.20,153.75,45000000
2023-01-04,153.80,158.00,152.50,157.20,52000000
2023-01-05,157.00,159.50,155.80,158.90,48000000
2023-01-06,158.50,162.00,157.00,161.25,51000000
2023-01-09,161.30,165.00,160.50,164.80,55000000
```

### Upload Steps
1. Navigate to **CSV Upload** page
2. Click "Browse files" or drag-and-drop your CSV
3. Wait for validation
4. Go to **Stock Analysis** to visualize
5. Go to **ML Predictions** to train models

---

## 🎛️ Dashboard Usage

### Sidebar Controls
| Control | Description |
|---------|-------------|
| **Stock Ticker** | Enter stock symbol (e.g., AAPL) |
| **Historical Period** | Choose data range (1mo to 5y) |
| **Navigation** | Switch between app pages |

### Page Descriptions
| Page | Purpose |
|------|---------|
| **Home** | Overview and quick start guide |
| **Stock Analysis** | Candlestick charts, volume, indicators |
| **ML Predictions** | Train models, view predictions, residuals |
| **Model Comparison** | Compare all 4 ML models side-by-side |
| **Future Forecast** | Next-day and multi-day price forecasts |
| **CSV Upload** | Use your own custom dataset |
| **About** | Project info and disclaimer |

### Interactive Features
- **Hover** over charts for detailed tooltips
- **Zoom** on Plotly charts using mouse wheel
- **Pan** by dragging on chart area
- **Download** data as CSV from any table
- **Toggle** traces on charts via legend

---

## 📊 Analytics Explanation

### Key Metrics

| Metric | Description | Interpretation |
|--------|-------------|----------------|
| **Daily Return** | % change from previous close | Positive = gain, Negative = loss |
| **Volatility** | Standard deviation of returns | Higher = more risk/uncertainty |
| **Moving Average (MA)** | Average price over N days | Price above MA = uptrend |
| **RSI** | Relative Strength Index (0-100) | >70 overbought, <30 oversold |
| **MACD** | Moving Average Convergence Divergence | Crossover signals trend change |
| **Bollinger Bands** | Price envelope (±2 std dev) | Price near upper = overbought |

### ML Metrics

| Metric | Description | Good Value |
|--------|-------------|------------|
| **R² Score** | Variance explained by model | Closer to 1.0 is better |
| **MAE** | Mean Absolute Error ($) | Lower is better |
| **RMSE** | Root Mean Squared Error ($) | Lower is better |
| **MAPE** | Mean Absolute % Error | <10% is excellent |

---

## 🛠️ Troubleshooting

### Issue: "Could not fetch data for [ticker]"
**Solution:**
- Check if ticker symbol is valid
- Try a different ticker (e.g., AAPL, MSFT)
- Ensure internet connection is active
- Use the local `stock_dataset.csv` instead

### Issue: "Insufficient data"
**Solution:**
- Select a longer historical period (e.g., 1y or 2y)
- The model needs at least 50 data points
- Check if the stock has been trading long enough

### Issue: "Module not found" error
**Solution:**
- Run `install.sh` (Linux) or `install.bat` (Windows)
- Ensure virtual environment is activated
- Try: `pip install -r requirements.txt`

### Issue: Streamlit not launching
**Solution:**
- Verify Python 3.11+ is installed
- Run: `streamlit run app.py` manually
- Check if port 8501 is available

### Issue: Slow model training
**Solution:**
- This is normal for Random Forest with 200 estimators
- Reduce historical period for faster training
- Ensure your system has sufficient RAM

### Issue: Predictions seem inaccurate
**Solution:**
- Stock markets are inherently unpredictable
- Use longer historical periods for better training
- Compare multiple models in Model Comparison
- Remember: this is for educational purposes only

### Issue: CSS not loading
**Solution:**
- Ensure `assets/styles.css` exists in project folder
- Restart Streamlit app
- Check browser console for errors

---

## 💡 Pro Tips

1. **Compare multiple tickers** by switching in the sidebar
2. **Use 2y+ data** for more accurate ML models
3. **Check Model Comparison** before trusting predictions
4. **Download forecasts** to analyze offline
5. **Upload your own CSV** for private/unlisted stocks
6. **Read the AI Explanation** for market context

---

*For more help, visit the [GitHub Repository](https://github.com/issu321/Stock-Price-Prediction-Using-Machine-Learning)*

*Developed by [issu321](https://github.com/issu321)*
