from ingestion import fetch_data
from cleaner import clean_data
from volatility import calculate_volatility
from plotter import plot_volatility

def run_pipeline(ticker, period="1y"):
    # 1. fetch
    df = fetch_data(ticker, period=period)
    # 2. clean
    df = clean_data(df)
    # 3. calculate volatility
    df = calculate_volatility(df)
    # 4. plot
    plot_volatility(df, ticker=ticker)

if __name__ == "__main__":
    run_pipeline("AAPL")