import pandas as pd
import numpy as np

def calculate_volatility(df, window=21):
    df["daily_log_return"] = np.log(df["Close"] / df["Close"].shift(1))
    df["rolling_std"] = df["daily_log_return"].rolling(window=window).std()
    df["volatility"] = df["rolling_std"].mul(np.sqrt(252))
    return df

if __name__ == "__main__":
    from ingestion import fetch_data
    from cleaner import clean_data

    df = fetch_data("AAPL")
    df = clean_data(df)
    df = calculate_volatility(df)
    print(df[["Close", "volatility"]].tail(10))