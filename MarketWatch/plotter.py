import matplotlib.pyplot as plt

def plot_volatility(df):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), sharex=True)

    for ticker, g in df.groupby("ticker"):
        ax1.plot(g["Date"], g["Close"], label=ticker)
        ax2.plot(g["Date"], g["volatility"], label=ticker)

    ax1.set_title("Price")
    ax1.set_ylabel("Close ($)")
    ax1.legend()

    ax2.set_title("Annualized Volatility")
    ax2.set_ylabel("Volatility")
    ax2.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    from ingestion import fetch_many
    from cleaner import clean_data
    from volatility import calculate_volatility

    df = fetch_many(["AAPL", "MSFT", "SPY"])
    df = clean_data(df)
    df = calculate_volatility(df)
    plot_volatility(df)