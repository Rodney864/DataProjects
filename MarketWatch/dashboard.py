import streamlit as st
import pandas as pd

from ingestion import fetch_many
from cleaner import clean_data
from database import save_data, load_data, query
from volatility import calculate_volatility
from risk import compute_var

st.set_page_config(page_title="Equity Risk Analytics", layout="wide")
st.title("📈 Equity Risk Analytics Dashboard")

# --- Session state init ---
if "df" not in st.session_state:
    st.session_state.df = None

# --- Sidebar ---
st.sidebar.header("Settings")
tickers = st.sidebar.text_input("Tickers (space-separated)", "AAPL MSFT SPY").upper().split()
period = st.sidebar.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)
window = st.sidebar.slider("Volatility window (days)", 5, 120, 21)

if st.sidebar.button("Fetch & Store Data"):
    if not tickers:
        st.error("Please enter at least one ticker.")
        st.stop()
    with st.spinner("Fetching, storing, and analyzing..."):
        try:
            df = fetch_many(tickers, period=period)
            df = clean_data(df)
            save_data(df)
            df = load_data(tickers)
            df = calculate_volatility(df, window=window)
            st.session_state.df = df
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.stop()

# --- Render dashboard (persists across reruns) ---
df = st.session_state.df
if df is not None:
    st.success(
        f"Loaded {len(df)} rows across {df['ticker'].nunique()} tickers"
    )

    # Price chart (native)
    st.subheader("Price")
    st.line_chart(df.pivot(index="Date", columns="ticker", values="Close"))

    # Volatility chart
    st.subheader(f"Annualized Volatility ({window}-day window)")
    st.line_chart(df.pivot(index="Date", columns="ticker", values="volatility"))

    # --- Value at Risk ---
    st.subheader("Value at Risk (Historical Method)")
    col1, col2 = st.columns(2)
    confidence = col1.selectbox("Confidence level", [0.90, 0.95, 0.99], index=1)
    position = col2.number_input("Position size per ticker ($)", value=10000, step=1000)

    var_table = compute_var(df, confidence=confidence)
    var_table["VaR ($)"] = (var_table["VaR_pct"] * position).round(2)
    var_table["CVaR ($)"] = (var_table["CVaR_pct"] * position).round(2)

    display = var_table[["ticker", "VaR_pct", "CVaR_pct", "VaR ($)", "CVaR ($)"]].rename(
        columns={"VaR_pct": "VaR (%)", "CVaR_pct": "CVaR (%)"}
    )
    st.dataframe(
        display.style.format({
            "VaR (%)": "{:.2%}", "CVaR (%)": "{:.2%}",
            "VaR ($)": "${:,.2f}", "CVaR ($)": "${:,.2f}",
        }),
        use_container_width=True,
    )
    st.caption(
        f"At {confidence:.0%} confidence: VaR is the loss threshold on the worst "
        f"{(1-confidence):.0%} of days. CVaR is the average loss on those worst days."
    )

    # SQL summary
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
    st.dataframe(summary, use_container_width=True)
else:
    st.info("👈 Configure settings and click **Fetch & Store Data** to begin.")