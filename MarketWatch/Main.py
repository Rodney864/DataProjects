from ingestion import fetch_many
from cleaner import clean_data
from database import save_data, load_data
from volatility import calculate_volatility
from plotter import plot_volatility


def run_pipeline(tickers, period="1y", window=21):
    # 1. Fetch + clean
    df = fetch_many(tickers, period=period)
    df = clean_data(df)

    # 2. Persist to SQL database
    save_data(df)

    # 3. Read back FROM SQL (mirrors real-world: analysis queries the DB)
    df = load_data(tickers)

    # 4. Analyze + plot
    df = calculate_volatility(df, window=window)
    plot_volatility(df)
    return df


if __name__ == "__main__":
    run_pipeline(["AAPL", "MSFT", "SPY"])