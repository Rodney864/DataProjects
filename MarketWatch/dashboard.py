import streamlit as st
import matplotlib.pyplot as plt

from ingestion import fetch_many
from cleaner import clean_data
from database import save_data, load_data, query
from volatility import calculate_volatility
from risk import compute_var

st.set_page_config(page_title="Equity Risk Analytics", layout="wide")
st.title("📈 Equity Risk Analytics Dashboard")

# Sidebar 
st.sidebar.header("Settings")
tickers = st.sidebar.text_input("Tickers (space-separated)", "AAPL MSFT SPY").upper().split()
period = st.sidebar.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
window = st.sidebar.slider("Volatility window (days)", 5, 120, 21)

if st.sidebar.button("Fetch & Store Data"):
    if not tickers:
        st.error("Please enter at least one ticker.")
        st.stop()

    with st.spinner("Fetching, storing in database, and analyzing..."):
        try:
            # 1. Fetch + clean
            df = fetch_many(tickers, period=period)
            df = clean_data(df)
            # 2. Save to SQL
            save_data(df)
            # 3. Load back FROM SQL
            df = load_data(tickers)
            # 4. Analyze
            df = calculate_volatility(df, window=window)
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.stop()

    st.success(f"Stored & loaded {len(df)} rows from database across {df['ticker'].nunique()} tickers")

    # Price chart
    st.subheader("Price")
    fig1, ax1 = plt.subplots(figsize=(11, 4))
    for tk, g in df.groupby("ticker"):
        ax1.plot(g["Date"], g["Close"], label=tk)
    ax1.set_ylabel("Close ($)")
    ax1.legend()
    st.pyplot(fig1)

    # Volatility chart
    st.subheader(f"Annualized Volatility ({window}-day window)")
    fig2, ax2 = plt.subplots(figsize=(11, 4))
    for tk, g in df.groupby("ticker"):
        ax2.plot(g["Date"], g["volatility"], label=tk)
    ax2.set_ylabel("Volatility")
    ax2.legend()
    st.pyplot(fig2)

    # --- Value at Risk ---
    st.subheader("Value at Risk (Historical Method)")

    col1, col2 = st.columns(2)
    confidence = col1.selectbox("Confidence level", [0.90, 0.95, 0.99], index=1)
    position = col2.number_input("Position size per ticker ($)", value=10000, step=1000)

    var_table = compute_var(df, confidence=confidence)
    var_table["VaR ($)"] = (var_table["VaR_pct"] * position).round(2)
    var_table["CVaR ($)"] = (var_table["CVaR_pct"] * position).round(2)

    display = var_table[["ticker", "VaR_pct", "CVaR_pct", "VaR ($)", "CVaR ($)"]].copy()
    display = display.rename(columns={"VaR_pct": "VaR (%)", "CVaR_pct": "CVaR (%)"})

    st.dataframe(
        display.style.format({
            "VaR (%)": "{:.2%}", "CVaR (%)": "{:.2%}",
            "VaR ($)": "${:,.2f}", "CVaR ($)": "${:,.2f}",
        })
    )

    st.caption(
        f"At {confidence:.0%} confidence: VaR is the loss threshold on the worst "
        f"{(1-confidence):.0%} of days. CVaR is the *average* loss on those worst days."
    )
    
        # SQL-powered summary table 
    st.subheader("Summary Statistics (via SQL)")
    summary = query("""
        SELECT ticker,
               ROUND(AVG(Close), 2) AS avg_close,
               ROUND(MAX(Close), 2) AS high,
               ROUND(MIN(Close), 2) AS low,
               COUNT(*) AS trading_days
        FROM prices
        GROUP BY ticker
        ORDER BY avg_close DESC
    """)
    st.dataframe(summary)