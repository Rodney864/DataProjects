import matplotlib.pyplot as plt

def plot_volatility(df, ticker="AAPL"):
    fig, (ax1, ax2) = plt.subplots(2,1, figsize=(12, 6), sharex= True)

    ax1.plot(df.index, df['Close'], label='Close')
    ax1.set_title(f"{ticker} - Price")
    ax2.plot(df.index, df['volatility'], label='volatility')
    ax2.set_title(f"{ticker} - volatility")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    from ingestion import fetch_data
    from cleaner import clean_data
    from volatility import calculate_volatility

    df = fetch_data("AAPL")
    df = clean_data(df)
    df = calculate_volatility(df)
    plot_volatility(df)