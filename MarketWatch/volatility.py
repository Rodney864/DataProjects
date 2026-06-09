import numpy as np


def calculate_volatility(df, window=21):
    df = df.copy()
    df["daily_log_return"] = (
        df.groupby("ticker")["Close"]
        .transform(lambda s: np.log(s / s.shift(1)))
    )
    df["volatility"] = (
        df.groupby("ticker")["daily_log_return"]
        .transform(lambda s: s.rolling(window).std() * np.sqrt(252))
    )
    return df

if __name__ == "__main__":
    from ingestion import fetch_data
    from cleaner import clean_data

    df = fetch_data("AAPL")
    df = clean_data(df)
    df = df.reset_index()          
    df["ticker"] = "AAPL"         
    df = calculate_volatility(df)
    print(df[["Close", "volatility"]].tail(10))