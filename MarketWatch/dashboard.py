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
# Store the RAW loaded data (no volatility yet) so we can recompute
# volatility live when the user changes the window slider.
if "raw_df" not in st.session_state:
    st.session_state.raw_df = None
if "loaded_tickers" not in st.session_state:
    st.session_state.loaded_tickers = []

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
            # Load back from SQL (mirrors real-world: analysis queries the DB)
            st.session_state.raw_df = load_data(tickers)
            st.session_state.loaded_tickers = tickers
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.stop()

# --- Render dashboard (persists across reruns) ---
raw_df = st.session_state.raw_df
loaded_tickers = st.session_state.loaded_tickers

if raw_df is not None and loaded_tickers:
    # Recompute volatility live with the CURRENT slider value.
    # No re-fetch needed — moving the slider updates the chart instantly.
    df = calculate_volatility(raw_df, window=window)

    st.success(
        f"Loaded {len(df)} rows across {df['ticker'].nunique()} tickers"
    )

    # --- Price chart ---
    # Normalized view lets you compare tickers at different price levels
    # (e.g. AAPL ~$200 vs SPY ~$580) on a fair, common scale.
    st.subheader("Price")
    price_pivot = df.pivot_table(
        index="Date", columns="ticker", values="Close", aggfunc="last"
    )

    view = st.radio(
        "View",
        ["Normalized (% performance)", "Raw price ($)"],
        horizontal=True,
    )
    if view.startswith("Normalized"):
        normalized = price_pivot / price_pivot.iloc[0] * 100
        st.line_chart(normalized)
        st.caption("Each ticker rebased to 100 at the start of the period — shows relative performance.")
    else:
        st.line_chart(price_pivot)
        st.caption("Raw closing prices in dollars.")

    # --- Volatility chart ---
    st.subheader(f"Annualized Volatility ({window}-day window)")
    vol_pivot = df.pivot_table(
        index="Date", columns="ticker", values="volatility", aggfunc="last"
    )
    st.line_chart(vol_pivot)

    # --- Value at Risk ---
    st.subheader("Value at Risk (Historical Method)")
    col1, col2 = st.columns(2)
    confidence = col1.selectbox("Confidence level", [0.90, 0.95, 0.99], index=1)
    position = col2.number_input("Position size per ticker ($)", value=10000.0, step=1000.0)

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
        width='stretch',
    )
    st.caption(
        f"At {confidence:.0%} confidence: VaR is the loss threshold on the worst "
        f"{(1 - confidence):.0%} of days. CVaR is the average loss on those worst days."
    )

    # --- SQL summary (parameterized to the loaded tickers) ---
    st.subheader("Summary Statistics (via SQL)")
    placeholders = ",".join("?" for _ in loaded_tickers)
    summary = query(
        f"""
        SELECT ticker,
               ROUND(AVG(Close), 2) AS avg_close,
               ROUND(MAX(Close), 2) AS high,
               ROUND(MIN(Close), 2) AS low,
               COUNT(*) AS trading_days
        FROM prices
        WHERE ticker IN ({placeholders})
        GROUP BY ticker
        ORDER BY avg_close DESC
        """,
        params=loaded_tickers,
    )
    st.dataframe(summary, width='stretch')

else:
    st.info("👈 Configure settings and click **Fetch & Store Data** to begin.")