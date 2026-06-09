import yfinance as yf
import pandas as pd

def fetch_data(ticker, period="1y"):
    stock = yf.Ticker(ticker)
    return stock.history(period=period)

def fetch_many(tickers, period="1y"):
    """Fetch multiple tickers into one tidy DataFrame with a 'ticker' column."""
    frames = []
    for tk in tickers:
        df = fetch_data(tk, period=period)
        if df.empty:
            print(f"⚠️  No data for {tk}, skipping.")
            continue
        df = df.reset_index()          
        df["ticker"] = tk
        frames.append(df)
    return pd.concat(frames, ignore_index=True)