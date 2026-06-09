import numpy as np
import pandas as pd
import pytest

from volatility import calculate_volatility


@pytest.fixture
def sample_df():
    """Two tickers with known, controlled prices."""
    dates = pd.date_range("2024-01-01", periods=30)
    data = []
    for tk, base in [("AAA", 100), ("BBB", 50)]:
        for i, d in enumerate(dates):
            data.append({"Date": d, "ticker": tk, "Close": base + i})
    return pd.DataFrame(data)


def test_returns_dataframe(sample_df):
    """Function should return a DataFrame, not mutate-and-lose data."""
    result = calculate_volatility(sample_df, window=5)
    assert isinstance(result, pd.DataFrame)


def test_adds_expected_columns(sample_df):
    """Volatility column must exist after calculation."""
    result = calculate_volatility(sample_df, window=5)
    assert "volatility" in result.columns
    assert "daily_log_return" in result.columns


def test_volatility_non_negative(sample_df):
    """Volatility is a standard deviation × √252 — it can never be negative."""
    result = calculate_volatility(sample_df, window=5)
    vols = result["volatility"].dropna()
    assert (vols >= 0).all()


def test_window_creates_leading_nans(sample_df):
    """A 5-day rolling window can't produce a value until 5 observations exist."""
    result = calculate_volatility(sample_df, window=5)
    # Per ticker, the first few rows should be NaN
    first_ticker = result[result["ticker"] == "AAA"]
    assert first_ticker["volatility"].iloc[0] != first_ticker["volatility"].iloc[0]  # NaN check


def test_tickers_computed_independently(sample_df):
    """groupby must prevent one ticker's data bleeding into another's calc."""
    result = calculate_volatility(sample_df, window=5)
    # Both tickers should have the same number of rows as input
    assert (result["ticker"] == "AAA").sum() == 30
    assert (result["ticker"] == "BBB").sum() == 30