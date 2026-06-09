import numpy as np
import pandas as pd


def compute_var(df: pd.DataFrame, confidence: float = 0.95) -> pd.DataFrame:
    """
    Historical VaR and CVaR per ticker, based on daily returns.

    Returns are expressed as the loss threshold:
      - VaR  = the return at the (1 - confidence) percentile
      - CVaR = the average return *beyond* that percentile (the tail)
    Values are negative (they represent losses).
    """
    df = df.copy().sort_values(["ticker", "Date"])
    df["daily_return"] = df.groupby("ticker")["Close"].pct_change()

    alpha = 1 - confidence  # e.g. 0.05 for 95% confidence
    results = []

    for ticker, g in df.groupby("ticker"):
        returns = g["daily_return"].dropna()
        if returns.empty:
            continue

        var = np.percentile(returns, alpha * 100)        # 5th percentile return
        cvar = returns[returns <= var].mean()            # avg of the worst tail

        results.append({
            "ticker": ticker,
            "confidence": confidence,
            "VaR_pct": var,           # e.g. -0.023  → worst 5% days lose ≥2.3%
            "CVaR_pct": cvar,         # e.g. -0.035  → those days avg -3.5%
            "obs": len(returns),
        })

    return pd.DataFrame(results)


def dollar_var(var_pct: float, position_value: float) -> float:
    """Convert a percentage VaR into a dollar figure for a given position size."""
    return var_pct * position_value


if __name__ == "__main__":
    from ingestion import fetch_many
    from cleaner import clean_data

    df = fetch_many(["AAPL", "MSFT", "SPY"])
    df = clean_data(df)

    var_table = compute_var(df, confidence=0.95)
    print(var_table)

    # Example: $10,000 invested in each
    var_table["VaR_$10k"] = var_table["VaR_pct"].apply(lambda v: dollar_var(v, 10_000))
    print(var_table[["ticker", "VaR_pct", "VaR_$10k"]])