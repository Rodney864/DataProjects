import yfinance as yf

def fetch_data(ticker, period="1y"):
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    return df

if __name__ == "__main__":
    df = fetch_data("AAPL")
    print(df.head())
    print(df.shape)