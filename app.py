import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="NeuralTrade AI | Stock Price Prediction",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS - CYBERPUNK THEME
# ============================================================
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #0a0a0a 0%, #111827 50%, #0a0a0a 100%); }
        .main-header { color: #00f0ff; text-align: center; font-size: 2.8rem; font-weight: 800; text-shadow: 0 0 20px #00f0ff; }
        .sub-header { color: #a78bfa; text-align: center; font-size: 1.1rem; margin-bottom: 2rem; }
        .metric-card { background: rgba(17,24,39,0.85); border: 1px solid #00f0ff; border-radius: 12px; padding: 1rem; box-shadow: 0 0 15px rgba(0,240,255,0.15); }
        .metric-label { color: #94a3b8; font-size: 0.85rem; }
        .metric-value { color: #00f0ff; font-size: 1.6rem; font-weight: 700; }
        .stButton>button { background: linear-gradient(90deg, #00f0ff, #a78bfa); color: #000; font-weight: 700; border: none; border-radius: 8px; }
        .stButton>button:hover { box-shadow: 0 0 20px rgba(0,240,255,0.5); transform: translateY(-2px); }
        .sidebar-title { color: #00f0ff; font-size: 1.3rem; font-weight: 700; text-shadow: 0 0 10px #00f0ff; }
        .footer { text-align: center; color: #64748b; padding: 2rem; border-top: 1px solid #1e293b; margin-top: 3rem; }
        .footer a { color: #00f0ff; text-decoration: none; }
        .footer a:hover { text-shadow: 0 0 10px #00f0ff; }
        .prediction-card { background: rgba(17,24,39,0.9); border: 1px solid #a78bfa; border-radius: 16px; padding: 2rem; box-shadow: 0 0 25px rgba(167,139,250,0.2); }
        .positive { color: #34d399; }
        .negative { color: #f87171; }
        .info-box { background: rgba(0,240,255,0.08); border-left: 3px solid #00f0ff; padding: 1rem; border-radius: 0 8px 8px 0; margin: 1rem 0; }
        </style>
        """, unsafe_allow_html=True)

load_css()

# ============================================================
# SESSION STATE
# ============================================================
if "data" not in st.session_state:
    st.session_state.data = None
if "models" not in st.session_state:
    st.session_state.models = {}
if "best_model" not in st.session_state:
    st.session_state.best_model = None
if "scaler" not in st.session_state:
    st.session_state.scaler = None
if "features" not in st.session_state:
    st.session_state.features = None
if "target" not in st.session_state:
    st.session_state.target = None

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="main-header">📈 NeuralTrade AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Advanced Machine Learning Stock Price Prediction System</div>', unsafe_allow_html=True)
st.markdown("---")

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">⚙️ Control Panel</div>', unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio("Navigation", [
        "🏠 Home",
        "📊 Stock Analysis",
        "🤖 ML Predictions",
        "📉 Model Comparison",
        "🔮 Future Forecast",
        "📁 CSV Upload",
        "ℹ️ About"
    ], index=0)

    st.markdown("---")
    st.markdown("**Quick Settings**")

    ticker = st.text_input("Stock Ticker", value="AAPL", max_chars=10).upper().strip()
    period = st.selectbox("Historical Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

    st.markdown("---")
    st.markdown('<div style="text-align:center; font-size:0.8rem; color:#64748b;">Developed by <a href="https://github.com/issu321" target="_blank" style="color:#00f0ff;">issu321</a></div>', unsafe_allow_html=True)

# ============================================================
# DATA FETCHING - ROBUST VERSION
# ============================================================
@st.cache_data(ttl=3600)
def fetch_stock_data(ticker, period="1y"):
    try:
        data = yf.download(ticker, period=period, progress=False)
        if data is None or data.empty:
            return None

        # Flatten MultiIndex columns if present (newer yfinance versions)
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [c[0] if isinstance(c, tuple) else c for c in data.columns]

        # Reset index to get datetime as a column
        data = data.reset_index()

        # Robustly find and rename the datetime column
        # yfinance index names vary: 'Date', 'Datetime', or unnamed
        date_col = None
        for col in data.columns:
            col_str = str(col).lower()
            if 'date' in col_str or 'datetime' in col_str:
                date_col = col
                break

        if date_col is not None and date_col != "Date":
            data = data.rename(columns={date_col: "Date"})

        # If still no Date column, create one from the first column if it's datetime
        if "Date" not in data.columns:
            for col in data.columns:
                if pd.api.types.is_datetime64_any_dtype(data[col]):
                    data = data.rename(columns={col: "Date"})
                    break

        # Ensure required price columns exist
        for col in ["Open", "High", "Low", "Close", "Volume"]:
            if col not in data.columns:
                if col == "Volume":
                    data[col] = 0
                elif "Close" in data.columns:
                    data[col] = data["Close"]
                else:
                    data[col] = 0.0

        # Ensure Date column exists
        if "Date" not in data.columns:
            # Last resort: create a synthetic date range
            data["Date"] = pd.date_range(end=datetime.today(), periods=len(data), freq="B")

        # Ensure Date is datetime type
        data["Date"] = pd.to_datetime(data["Date"])

        return data
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

def load_local_csv():
    path = os.path.join(os.path.dirname(__file__), "stock_dataset.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        if "Date" not in df.columns:
            # Try to find any date-like column
            for col in df.columns:
                if 'date' in str(col).lower():
                    df = df.rename(columns={col: "Date"})
                    break
        df["Date"] = pd.to_datetime(df["Date"])
        return df
    return None

# ============================================================
# FEATURE ENGINEERING - ROBUST VERSION
# ============================================================
def engineer_features(df):
    df = df.copy()

    # Ensure Date column exists
    if "Date" not in df.columns:
        raise ValueError("DataFrame must contain a 'Date' column. Available columns: " + str(list(df.columns)))

    df = df.sort_values("Date").reset_index(drop=True)

    # Ensure numeric columns
    numeric_cols = ["Open", "High", "Low", "Close", "Volume"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows where Close is NaN
    df = df.dropna(subset=["Close"]).reset_index(drop=True)

    if len(df) < 20:
        return df

    # Price-based features
    df["Daily_Return"] = df["Close"].pct_change()
    df["Price_Range"] = df["High"] - df["Low"]
    df["Price_Change"] = df["Close"] - df["Open"]

    # Moving averages
    for window in [5, 10, 20, 50]:
        if len(df) >= window:
            df[f"MA_{window}"] = df["Close"].rolling(window=window).mean()
            df[f"EMA_{window}"] = df["Close"].ewm(span=window, adjust=False).mean()

    # Volatility
    if len(df) >= 5:
        df["Volatility_5"] = df["Daily_Return"].rolling(window=5).std()
    if len(df) >= 20:
        df["Volatility_20"] = df["Daily_Return"].rolling(window=20).std()

    # Lag features
    for lag in [1, 2, 3, 5]:
        if len(df) > lag:
            df[f"Close_Lag_{lag}"] = df["Close"].shift(lag)
            if "Volume" in df.columns:
                df[f"Volume_Lag_{lag}"] = df["Volume"].shift(lag)

    # RSI
    if len(df) >= 15:
        delta = df["Close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = (-delta).where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss.replace(0, np.nan)
        df["RSI"] = 100 - (100 / (1 + rs))

    # MACD
    if len(df) >= 35:
        ema12 = df["Close"].ewm(span=12, adjust=False).mean()
        ema26 = df["Close"].ewm(span=26, adjust=False).mean()
        df["MACD"] = ema12 - ema26
        df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    # Bollinger Bands
    if len(df) >= 20:
        df["BB_Middle"] = df["Close"].rolling(window=20).mean()
        bb_std = df["Close"].rolling(window=20).std()
        df["BB_Upper"] = df["BB_Middle"] + (bb_std * 2)
        df["BB_Lower"] = df["BB_Middle"] - (bb_std * 2)

    df = df.dropna().reset_index(drop=True)
    return df

# ============================================================
# ML PIPELINE
# ============================================================
def prepare_ml_data(df, target_col="Close", test_size=0.2):
    feature_cols = [
        "Open", "High", "Low", "Volume",
        "Daily_Return", "Price_Range", "Price_Change",
        "MA_5", "MA_10", "MA_20", "MA_50",
        "EMA_5", "EMA_10", "EMA_20", "EMA_50",
        "Volatility_5", "Volatility_20",
        "Close_Lag_1", "Close_Lag_2", "Close_Lag_3", "Close_Lag_5",
        "Volume_Lag_1", "Volume_Lag_2", "Volume_Lag_3", "Volume_Lag_5",
        "RSI", "MACD", "MACD_Signal",
        "BB_Middle", "BB_Upper", "BB_Lower"
    ]

    available_features = [c for c in feature_cols if c in df.columns]
    if len(available_features) < 3:
        st.error(f"Not enough features available. Found: {available_features}")
        return None, None, None, None, None, None

    X = df[available_features].values
    y = df[target_col].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=test_size, shuffle=False
    )

    return X_train, X_test, y_train, y_test, scaler, available_features

def train_models(X_train, X_test, y_train, y_test):
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1),
        "Decision Tree": DecisionTreeRegressor(max_depth=15, random_state=42),
        "Support Vector": SVR(kernel="rbf", C=100, gamma="scale")
    }

    results = {}
    trained_models = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mape = np.mean(np.abs((y_test - y_pred) / (y_test + 1e-8))) * 100

        results[name] = {
            "R² Score": r2,
            "MAE": mae,
            "RMSE": rmse,
            "MAPE": mape,
            "Predictions": y_pred
        }
        trained_models[name] = model

    best_name = max(results, key=lambda k: results[k]["R² Score"])

    return trained_models, results, best_name

def save_best_model(model, scaler, features, ticker):
    model_data = {
        "model": model,
        "scaler": scaler,
        "features": features,
        "ticker": ticker,
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    path = os.path.join(os.path.dirname(__file__), "best_model.pkl")
    joblib.dump(model_data, path)
    return path

def load_best_model():
    path = os.path.join(os.path.dirname(__file__), "best_model.pkl")
    if os.path.exists(path):
        return joblib.load(path)
    return None

# ============================================================
# AI EXPLANATION ENGINE
# ============================================================
def generate_explanation(df, predictions, ticker):
    latest_close = float(df["Close"].iloc[-1])
    prev_close = float(df["Close"].iloc[-2]) if len(df) > 1 else latest_close
    change = latest_close - prev_close
    pct_change = (change / (prev_close + 1e-8)) * 100

    ma20 = df["MA_20"].iloc[-1] if "MA_20" in df.columns and not pd.isna(df["MA_20"].iloc[-1]) else latest_close
    ma50 = df["MA_50"].iloc[-1] if "MA_50" in df.columns and not pd.isna(df["MA_50"].iloc[-1]) else latest_close
    trend = "upward" if ma20 > ma50 else "downward"

    vol = df["Daily_Return"].std() * 100 if "Daily_Return" in df.columns else 0

    if vol < 1.5:
        vol_desc = "low volatility (stable)"
    elif vol < 3:
        vol_desc = "moderate volatility"
    else:
        vol_desc = "high volatility (risky)"

    rsi = float(df["RSI"].iloc[-1]) if "RSI" in df.columns and not pd.isna(df["RSI"].iloc[-1]) else 50
    if rsi > 70:
        rsi_desc = "overbought conditions"
    elif rsi < 30:
        rsi_desc = "oversold conditions"
    else:
        rsi_desc = "neutral momentum"

    pred_next = float(predictions[-1]) if len(predictions) > 0 else latest_close
    pred_direction = "rise" if pred_next > latest_close else "fall"

    explanation = f"""
    <div class="info-box">
    <h4 style="color:#00f0ff; margin-top:0;">🧠 AI Market Analysis for {ticker}</h4>
    <p><strong>Current Price:</strong> ${latest_close:.2f} ({"📈" if change >= 0 else "📉"} {pct_change:+.2f}%)</p>
    <p><strong>Trend:</strong> The stock shows a <span class="{'positive' if trend == 'upward' else 'negative'}">{trend}</span> trend over the recent period.</p>
    <p><strong>Volatility:</strong> Market exhibits <strong>{vol_desc}</strong> with {vol:.2f}% daily fluctuation.</p>
    <p><strong>Momentum (RSI):</strong> Currently in <strong>{rsi_desc}</strong> (RSI: {rsi:.1f}).</p>
    <p><strong>Prediction:</strong> ML models forecast the price will likely <span class="{'positive' if pred_direction == 'rise' else 'negative'}">{pred_direction}</span> to approximately <strong>${pred_next:.2f}</strong>.</p>
    </div>
    """
    return explanation

# ============================================================
# VISUALIZATION HELPERS
# ============================================================
def plot_candlestick(df, ticker):
    fig = go.Figure(data=[go.Candlestick(
        x=df["Date"],
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Price",
        increasing_line_color="#34d399",
        decreasing_line_color="#f87171"
    )])

    if "MA_20" in df.columns:
        fig.add_trace(go.Scatter(x=df["Date"], y=df["MA_20"], mode="lines", name="MA 20", line=dict(color="#00f0ff", width=1.5)))
    if "MA_50" in df.columns:
        fig.add_trace(go.Scatter(x=df["Date"], y=df["MA_50"], mode="lines", name="MA 50", line=dict(color="#a78bfa", width=1.5)))

    fig.update_layout(
        title=f"{ticker} Candlestick Chart with Moving Averages",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,24,39,0.5)",
        font=dict(color="#e2e8f0"),
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    return fig

def plot_volume(df, ticker):
    colors = ["#34d399" if df["Close"].iloc[i] >= df["Open"].iloc[i] else "#f87171" for i in range(len(df))]
    fig = go.Figure(data=[go.Bar(x=df["Date"], y=df["Volume"], marker_color=colors, name="Volume")])
    fig.update_layout(
        title=f"{ticker} Trading Volume",
        xaxis_title="Date",
        yaxis_title="Volume",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,24,39,0.5)",
        font=dict(color="#e2e8f0"),
        height=350
    )
    return fig

def plot_predictions(df, y_test, predictions, model_name, ticker):
    test_dates = df["Date"].iloc[-len(y_test):].reset_index(drop=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=test_dates, y=y_test, mode="lines", name="Actual", line=dict(color="#00f0ff", width=2)))
    fig.add_trace(go.Scatter(x=test_dates, y=predictions, mode="lines", name=f"Predicted ({model_name})", line=dict(color="#a78bfa", width=2, dash="dash")))
    fig.update_layout(
        title=f"{ticker} - Actual vs Predicted ({model_name})",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,24,39,0.5)",
        font=dict(color="#e2e8f0"),
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    return fig

def plot_model_comparison(results):
    models = list(results.keys())
    r2_scores = [results[m]["R² Score"] for m in models]
    maes = [results[m]["MAE"] for m in models]
    rmses = [results[m]["RMSE"] for m in models]

    fig = make_subplots(rows=1, cols=3, subplot_titles=("R² Score", "MAE", "RMSE"),
                        horizontal_spacing=0.08)

    colors = ["#00f0ff", "#a78bfa", "#34d399", "#f87171"]

    fig.add_trace(go.Bar(x=models, y=r2_scores, marker_color=colors, name="R²"), row=1, col=1)
    fig.add_trace(go.Bar(x=models, y=maes, marker_color=colors, name="MAE"), row=1, col=2)
    fig.add_trace(go.Bar(x=models, y=rmses, marker_color=colors, name="RMSE"), row=1, col=3)

    fig.update_layout(
        title="Model Performance Comparison",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,24,39,0.5)",
        font=dict(color="#e2e8f0"),
        height=400,
        showlegend=False
    )
    return fig

def plot_forecast(df, future_dates, forecast_values, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Date"], y=df["Close"], mode="lines", name="Historical", line=dict(color="#00f0ff", width=2)))
    fig.add_trace(go.Scatter(x=future_dates, y=forecast_values, mode="lines+markers", name="Forecast", line=dict(color="#a78bfa", width=2), marker=dict(size=8)))
    fig.update_layout(
        title=f"{ticker} - Future Price Forecast",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,24,39,0.5)",
        font=dict(color="#e2e8f0"),
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )
    return fig

# ============================================================
# PAGES
# ============================================================

# ---------- HOME ----------
if page == "🏠 Home":
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("""
        <div style="text-align:center; padding:2rem;">
        <h2 style="color:#00f0ff; text-shadow:0 0 15px #00f0ff;">Welcome to NeuralTrade AI</h2>
        <p style="color:#94a3b8; font-size:1.1rem;">
        A next-generation stock price prediction platform powered by machine learning.
        Analyze historical trends, compare ML models, and forecast future prices with confidence.
        </p>
        </div>
        """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="metric-card"><div class="metric-label">📊 Data Sources</div><div class="metric-value">yFinance</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><div class="metric-label">🤖 ML Models</div><div class="metric-value">4</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><div class="metric-label">⚡ Real-time</div><div class="metric-value">Live</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="metric-card"><div class="metric-label">🎯 Accuracy</div><div class="metric-value">R² + MAE</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(17,24,39,0.8); border:1px solid #1e293b; border-radius:16px; padding:2rem;">
    <h3 style="color:#a78bfa;">🚀 Quick Start Guide</h3>
    <ol style="color:#cbd5e1; line-height:2;">
    <li><strong>Enter a stock ticker</strong> (e.g., AAPL, TSLA, GOOGL) in the sidebar.</li>
    <li>Select your desired <strong>historical period</strong>.</li>
    <li>Navigate to <strong>Stock Analysis</strong> to visualize trends.</li>
    <li>Go to <strong>ML Predictions</strong> to train models and see forecasts.</li>
    <li>Visit <strong>Model Comparison</strong> to compare algorithm performance.</li>
    <li>Use <strong>Future Forecast</strong> for next-day and multi-day predictions.</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 **Tip:** Try tickers like AAPL, MSFT, TSLA, AMZN, NVDA, GOOGL, META, NFLX, AMD, INTC")

# ---------- STOCK ANALYSIS ----------
elif page == "📊 Stock Analysis":
    st.markdown("<h2 style='color:#00f0ff;'>📊 Stock Analysis Dashboard</h2>", unsafe_allow_html=True)

    data = fetch_stock_data(ticker, period)
    if data is None:
        st.warning(f"Could not fetch data for {ticker}. Using local dataset.")
        data = load_local_csv()

    if data is not None and not data.empty:
        st.session_state.data = data

        # Metrics
        latest = data.iloc[-1]
        prev = data.iloc[-2] if len(data) > 1 else latest

        close_val = float(latest.get("Close", 0))
        prev_close = float(prev.get("Close", close_val))
        change = close_val - prev_close
        pct = (change / (prev_close + 1e-8)) * 100
        vol_val = float(latest.get("Volume", 0))
        high_val = float(data["High"].max()) if "High" in data.columns else close_val
        low_val = float(data["Low"].min()) if "Low" in data.columns else close_val

        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Current Price</div><div class="metric-value">${close_val:.2f}</div></div>', unsafe_allow_html=True)
        with m2:
            color = "positive" if change >= 0 else "negative"
            st.markdown(f'<div class="metric-card"><div class="metric-label">Change</div><div class="metric-value {color}">{change:+.2f} ({pct:+.2f}%)</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Volume</div><div class="metric-value">{vol_val:,.0f}</div></div>', unsafe_allow_html=True)
        with m4:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Period High</div><div class="metric-value">${high_val:.2f}</div></div>', unsafe_allow_html=True)
        with m5:
            st.markdown(f'<div class="metric-card"><div class="metric-label">Period Low</div><div class="metric-value">${low_val:.2f}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Charts
        try:
            df_feat = engineer_features(data)
        except Exception as e:
            st.error(f"Feature engineering error: {e}")
            df_feat = data.copy()

        tab1, tab2, tab3, tab4 = st.tabs(["📈 Candlestick", "📊 Volume", "📉 Returns", "📐 Indicators"])

        with tab1:
            st.plotly_chart(plot_candlestick(df_feat, ticker), use_container_width=True)

        with tab2:
            st.plotly_chart(plot_volume(df_feat, ticker), use_container_width=True)

        with tab3:
            if "Daily_Return" in df_feat.columns:
                fig = px.line(df_feat, x="Date", y="Daily_Return", title="Daily Returns",
                              template="plotly_dark", color_discrete_sequence=["#00f0ff"])
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(17,24,39,0.5)", font=dict(color="#e2e8f0"), height=400)
                st.plotly_chart(fig, use_container_width=True)

                col_a, col_b = st.columns(2)
                with col_a:
                    ann_vol = df_feat["Daily_Return"].std() * np.sqrt(252) * 100 if df_feat["Daily_Return"].std() > 0 else 0
                    st.metric("Volatility (Annualized)", f"{ann_vol:.2f}%")
                with col_b:
                    st.metric("Max Daily Gain", f"{df_feat['Daily_Return'].max() * 100:.2f}%")
                    st.metric("Max Daily Loss", f"{df_feat['Daily_Return'].min() * 100:.2f}%")
            else:
                st.info("Daily returns not available for this dataset.")

        with tab4:
            if all(c in df_feat.columns for c in ["BB_Upper", "BB_Lower", "RSI", "MACD"]):
                fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                                    subplot_titles=("Bollinger Bands", "RSI & MACD"))
                fig.add_trace(go.Scatter(x=df_feat["Date"], y=df_feat["Close"], name="Close", line=dict(color="#00f0ff")), row=1, col=1)
                fig.add_trace(go.Scatter(x=df_feat["Date"], y=df_feat["BB_Upper"], name="BB Upper", line=dict(color="#a78bfa", dash="dash")), row=1, col=1)
                fig.add_trace(go.Scatter(x=df_feat["Date"], y=df_feat["BB_Lower"], name="BB Lower", line=dict(color="#a78bfa", dash="dash")), row=1, col=1)
                fig.add_trace(go.Scatter(x=df_feat["Date"], y=df_feat["RSI"], name="RSI", line=dict(color="#34d399")), row=2, col=1)
                fig.add_trace(go.Scatter(x=df_feat["Date"], y=df_feat["MACD"], name="MACD", line=dict(color="#f87171")), row=2, col=1)
                fig.add_trace(go.Scatter(x=df_feat["Date"], y=df_feat["MACD_Signal"], name="Signal", line=dict(color="#fbbf24", dash="dash")), row=2, col=1)
                fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(17,24,39,0.5)", font=dict(color="#e2e8f0"), height=600)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Technical indicators require more data. Try a longer period.")

        # Data table
        with st.expander("📋 View Raw Data"):
            st.dataframe(df_feat.tail(20), use_container_width=True)
            csv = df_feat.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download CSV", csv, f"{ticker}_data.csv", "text/csv")
    else:
        st.error("No data available. Please check the ticker symbol or upload a CSV file.")

# ---------- ML PREDICTIONS ----------
elif page == "🤖 ML Predictions":
    st.markdown("<h2 style='color:#00f0ff;'>🤖 Machine Learning Predictions</h2>", unsafe_allow_html=True)

    data = st.session_state.data
    if data is None:
        data = fetch_stock_data(ticker, period)
        if data is None:
            data = load_local_csv()
        st.session_state.data = data

    if data is not None and len(data) > 50:
        try:
            df_feat = engineer_features(data)
        except Exception as e:
            st.error(f"Feature engineering error: {e}")
            st.stop()

        if len(df_feat) < 30:
            st.error("Not enough data after feature engineering. Try a longer period.")
            st.stop()

        st.markdown("<div class='info-box'>Training 4 ML models on engineered features. This may take a few seconds...</div>", unsafe_allow_html=True)

        with st.spinner("Training models..."):
            ml_data = prepare_ml_data(df_feat)
            if ml_data[0] is None:
                st.stop()
            X_train, X_test, y_train, y_test, scaler, features = ml_data
            trained_models, results, best_name = train_models(X_train, X_test, y_train, y_test)

            st.session_state.models = trained_models
            st.session_state.best_model = trained_models[best_name]
            st.session_state.scaler = scaler
            st.session_state.features = features

        st.success(f"✅ Best Model: **{best_name}** (R² = {results[best_name]['R² Score']:.4f})")

        # Save model
        model_path = save_best_model(trained_models[best_name], scaler, features, ticker)
        st.info(f"💾 Best model saved to `{model_path}`")

        # AI Explanation
        best_preds = results[best_name]["Predictions"]
        st.markdown(generate_explanation(df_feat, best_preds, ticker), unsafe_allow_html=True)

        # Model selector
        selected_model = st.selectbox("Select Model to Visualize", list(results.keys()), index=list(results.keys()).index(best_name))

        # Metrics
        res = results[selected_model]
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="metric-card"><div class="metric-label">R² Score</div><div class="metric-value">{res["R² Score"]:.4f}</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><div class="metric-label">MAE</div><div class="metric-value">${res["MAE"]:.2f}</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="metric-card"><div class="metric-label">RMSE</div><div class="metric-value">${res["RMSE"]:.2f}</div></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="metric-card"><div class="metric-label">MAPE</div><div class="metric-value">{res["MAPE"]:.2f}%</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Prediction chart
        st.plotly_chart(plot_predictions(df_feat, y_test, res["Predictions"], selected_model, ticker), use_container_width=True)

        # Residuals
        with st.expander("📉 Residual Analysis"):
            residuals = y_test - res["Predictions"]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=res["Predictions"], y=residuals, mode="markers", marker=dict(color="#00f0ff", size=6, opacity=0.7), name="Residuals"))
            fig.add_hline(y=0, line_dash="dash", line_color="#f87171")
            fig.update_layout(title="Residual Plot", xaxis_title="Predicted", yaxis_title="Residual",
                              template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(17,24,39,0.5)", font=dict(color="#e2e8f0"), height=350)
            st.plotly_chart(fig, use_container_width=True)

            fig2 = go.Figure(data=[go.Histogram(x=residuals, marker_color="#a78bfa", nbinsx=30)])
            fig2.update_layout(title="Residual Distribution", xaxis_title="Residual", yaxis_title="Count",
                               template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(17,24,39,0.5)", font=dict(color="#e2e8f0"), height=300)
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.error("Insufficient data. Please fetch stock data first from Stock Analysis or check your ticker.")

# ---------- MODEL COMPARISON ----------
elif page == "📉 Model Comparison":
    st.markdown("<h2 style='color:#00f0ff;'>📉 Model Comparison</h2>", unsafe_allow_html=True)

    data = st.session_state.data
    if data is None:
        data = fetch_stock_data(ticker, period)
        if data is None:
            data = load_local_csv()
        st.session_state.data = data

    if data is not None and len(data) > 50:
        try:
            df_feat = engineer_features(data)
        except Exception as e:
            st.error(f"Feature engineering error: {e}")
            st.stop()

        if len(df_feat) < 30:
            st.error("Not enough data after feature engineering. Try a longer period.")
            st.stop()

        with st.spinner("Comparing all models..."):
            ml_data = prepare_ml_data(df_feat)
            if ml_data[0] is None:
                st.stop()
            X_train, X_test, y_train, y_test, scaler, features = ml_data
            trained_models, results, best_name = train_models(X_train, X_test, y_train, y_test)

        st.markdown(f"<div class='info-box'><strong>🏆 Winner:</strong> <span style='color:#00f0ff;'>{best_name}</span> with R² = {results[best_name]['R² Score']:.4f}</div>", unsafe_allow_html=True)

        # Comparison chart
        st.plotly_chart(plot_model_comparison(results), use_container_width=True)

        # Table
        st.markdown("<h3 style='color:#a78bfa;'>📊 Detailed Metrics</h3>", unsafe_allow_html=True)
        comp_df = pd.DataFrame({
            "Model": list(results.keys()),
            "R² Score": [f"{results[m]['R² Score']:.4f}" for m in results],
            "MAE ($)": [f"{results[m]['MAE']:.2f}" for m in results],
            "RMSE ($)": [f"{results[m]['RMSE']:.2f}" for m in results],
            "MAPE (%)": [f"{results[m]['MAPE']:.2f}" for m in results]
        })
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

        # Feature importance (Random Forest)
        if "Random Forest" in trained_models and features:
            rf = trained_models["Random Forest"]
            importances = rf.feature_importances_
            feat_imp = pd.DataFrame({"Feature": features, "Importance": importances}).sort_values("Importance", ascending=True).tail(min(15, len(features)))
            fig = go.Figure(go.Bar(x=feat_imp["Importance"], y=feat_imp["Feature"], orientation="h", marker_color="#00f0ff"))
            fig.update_layout(title="Top Feature Importances (Random Forest)", xaxis_title="Importance", yaxis_title="Feature",
                              template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(17,24,39,0.5)", font=dict(color="#e2e8f0"), height=500)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Insufficient data. Please fetch stock data first.")

# ---------- FUTURE FORECAST ----------
elif page == "🔮 Future Forecast":
    st.markdown("<h2 style='color:#00f0ff;'>🔮 Future Price Forecast</h2>", unsafe_allow_html=True)

    data = st.session_state.data
    if data is None:
        data = fetch_stock_data(ticker, period)
        if data is None:
            data = load_local_csv()
        st.session_state.data = data

    if data is not None and len(data) > 50:
        try:
            df_feat = engineer_features(data)
        except Exception as e:
            st.error(f"Feature engineering error: {e}")
            st.stop()

        if len(df_feat) < 30:
            st.error("Not enough data after feature engineering. Try a longer period.")
            st.stop()

        # Train if not already
        if st.session_state.best_model is None or st.session_state.scaler is None:
            with st.spinner("Training best model for forecasting..."):
                ml_data = prepare_ml_data(df_feat)
                if ml_data[0] is None:
                    st.stop()
                X_train, X_test, y_train, y_test, scaler, features = ml_data
                trained_models, results, best_name = train_models(X_train, X_test, y_train, y_test)
                st.session_state.models = trained_models
                st.session_state.best_model = trained_models[best_name]
                st.session_state.scaler = scaler
                st.session_state.features = features

        forecast_days = st.slider("Forecast Horizon (Days)", min_value=1, max_value=30, value=7)

        # Recursive forecasting
        last_row = df_feat.iloc[-1:].copy()
        future_dates = []
        forecast_values = []

        current_df = df_feat.copy()

        for i in range(forecast_days):
            next_date = current_df["Date"].iloc[-1] + timedelta(days=1)
            # Skip weekends
            while next_date.weekday() >= 5:
                next_date += timedelta(days=1)
            future_dates.append(next_date)

            # Create feature row from last known data
            feat_row = current_df[st.session_state.features].iloc[-1:].values
            feat_row_scaled = st.session_state.scaler.transform(feat_row)
            pred = st.session_state.best_model.predict(feat_row_scaled)[0]
            forecast_values.append(pred)

            # Append synthetic row for next iteration
            new_row = current_df.iloc[-1:].copy()
            new_row["Date"] = next_date
            new_row["Close"] = pred
            new_row["Open"] = pred * 0.995
            new_row["High"] = pred * 1.01
            new_row["Low"] = pred * 0.99
            new_row["Volume"] = float(current_df["Volume"].iloc[-10:].mean()) if "Volume" in current_df.columns else 0

            # Recompute simple lags
            new_row["Close_Lag_1"] = float(current_df["Close"].iloc[-1])
            new_row["Close_Lag_2"] = float(current_df["Close"].iloc[-2]) if len(current_df) > 1 else float(current_df["Close"].iloc[-1])
            new_row["Close_Lag_3"] = float(current_df["Close"].iloc[-3]) if len(current_df) > 2 else float(current_df["Close"].iloc[-1])
            new_row["Close_Lag_5"] = float(current_df["Close"].iloc[-5]) if len(current_df) > 4 else float(current_df["Close"].iloc[-1])

            current_df = pd.concat([current_df, new_row], ignore_index=True)

        st.markdown("<div class='prediction-card'>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:#a78bfa; margin-top:0;'>📅 {forecast_days}-Day Forecast for {ticker}</h3>", unsafe_allow_html=True)

        forecast_df = pd.DataFrame({"Date": future_dates, "Predicted_Close": forecast_values})
        st.dataframe(forecast_df.style.format({"Predicted_Close": "${:.2f}"}), use_container_width=True, hide_index=True)

        latest = float(data["Close"].iloc[-1])
        next_day = forecast_values[0]
        change = next_day - latest
        pct = (change / (latest + 1e-8)) * 100

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Price", f"${latest:.2f}")
        with col2:
            st.metric("Next Day Predicted", f"${next_day:.2f}", f"{change:+.2f} ({pct:+.2f}%)")
        with col3:
            st.metric(f"{forecast_days}-Day Target", f"${forecast_values[-1]:.2f}")

        st.markdown("</div>", unsafe_allow_html=True)

        # Chart
        st.plotly_chart(plot_forecast(data, future_dates, forecast_values, ticker), use_container_width=True)

        # Download
        csv = forecast_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Forecast CSV", csv, f"{ticker}_forecast.csv", "text/csv")
    else:
        st.error("Insufficient data. Please fetch stock data first.")

# ---------- CSV UPLOAD ----------
elif page == "📁 CSV Upload":
    st.markdown("<h2 style='color:#00f0ff;'>📁 Upload Custom Dataset</h2>", unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)

            # Robustly find date column
            date_col = None
            for col in df.columns:
                if 'date' in str(col).lower():
                    date_col = col
                    break

            if date_col and date_col != "Date":
                df = df.rename(columns={date_col: "Date"})

            if "Date" not in df.columns:
                st.error("CSV must contain a date column (e.g., 'Date', 'datetime').")
            elif "Close" not in df.columns:
                st.error("CSV must contain a 'Close' column.")
            else:
                df["Date"] = pd.to_datetime(df["Date"])
                st.session_state.data = df
                st.success(f"✅ Loaded {len(df)} rows from uploaded CSV.")
                st.dataframe(df.head(10), use_container_width=True)
                st.info("Navigate to Stock Analysis or ML Predictions to analyze this dataset.")
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
    else:
        st.markdown("""
        <div style="background:rgba(17,24,39,0.8); border:1px solid #1e293b; border-radius:12px; padding:1.5rem;">
        <h4 style="color:#a78bfa;">📋 Expected CSV Format</h4>
        <pre style="background:#0f172a; padding:1rem; border-radius:8px; color:#00f0ff; overflow-x:auto;">
Date,Open,High,Low,Close,Volume
2023-01-01,150.0,155.0,148.0,153.5,45000000
2023-01-02,153.5,158.0,152.0,157.2,52000000
...</pre>
        <p style="color:#94a3b8;">Required: <strong>Date</strong> and <strong>Close</strong>. Optional: Open, High, Low, Volume.</p>
        </div>
        """, unsafe_allow_html=True)

# ---------- ABOUT ----------
elif page == "ℹ️ About":
    st.markdown("""
    <div style="text-align:center; padding:2rem 0;">
    <h2 style="color:#00f0ff; text-shadow:0 0 15px #00f0ff;">ℹ️ About NeuralTrade AI</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(17,24,39,0.85); border:1px solid #1e293b; border-radius:16px; padding:2rem; margin-bottom:1.5rem;">
    <h3 style="color:#a78bfa;">🎯 Project Mission</h3>
    <p style="color:#cbd5e1; line-height:1.8;">
    NeuralTrade AI is a production-ready stock price prediction system designed to demonstrate
    the power of machine learning in financial analytics. Built with Python, Streamlit, and scikit-learn,
    it provides an intuitive interface for analyzing historical stock data, training multiple ML models,
    and generating actionable forecasts.
    </p>
    </div>

    <div style="background:rgba(17,24,39,0.85); border:1px solid #1e293b; border-radius:16px; padding:2rem; margin-bottom:1.5rem;">
    <h3 style="color:#a78bfa;">🛠️ Technologies Used</h3>
    <ul style="color:#cbd5e1; line-height:2;">
    <li><strong>Python 3.11+</strong> - Core language</li>
    <li><strong>Streamlit</strong> - Interactive web UI</li>
    <li><strong>yFinance</strong> - Real-time stock data</li>
    <li><strong>scikit-learn</strong> - Machine learning models</li>
    <li><strong>pandas & numpy</strong> - Data processing</li>
    <li><strong>plotly & matplotlib</strong> - Visualization</li>
    <li><strong>joblib</strong> - Model persistence</li>
    </ul>
    </div>

    <div style="background:rgba(17,24,39,0.85); border:1px solid #1e293b; border-radius:16px; padding:2rem; margin-bottom:1.5rem;">
    <h3 style="color:#a78bfa;">🤖 Machine Learning Models</h3>
    <ul style="color:#cbd5e1; line-height:2;">
    <li><strong>Linear Regression</strong> - Baseline model for trend capture</li>
    <li><strong>Random Forest Regressor</strong> - Ensemble method for robust predictions</li>
    <li><strong>Decision Tree Regressor</strong> - Interpretable rule-based model</li>
    <li><strong>Support Vector Regressor (SVR)</strong> - Kernel-based regression</li>
    </ul>
    </div>

    <div style="background:rgba(17,24,39,0.85); border:1px solid #1e293b; border-radius:16px; padding:2rem;">
    <h3 style="color:#a78bfa;">⚠️ Disclaimer</h3>
    <p style="color:#f87171; line-height:1.8;">
    <strong>This application is for educational and research purposes only.</strong>
    Stock predictions generated by machine learning models are not guaranteed to be accurate.
    Always consult a qualified financial advisor before making investment decisions.
    Past performance does not indicate future results.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="footer">
    <p>Developed by <a href="https://github.com/issu321" target="_blank">issu321</a></p>
    <p style="font-size:0.75rem;">NeuralTrade AI &copy; 2026 | Stock-Price-Prediction-Using-Machine-Learning</p>
    <p style="font-size:0.75rem;"><a href="https://github.com/issu321/Stock-Price-Prediction-Using-Machine-Learning" target="_blank">View on GitHub</a></p>
</div>
""", unsafe_allow_html=True)
