import numpy as np
import pandas as pd
import pytest

from risk import compute_var, dollar_var


@pytest.fixture
def known_returns_df():
    """
    Build prices whose returns we control.
    Using a fixed seed so the test is deterministic.
    """
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", periods=300)
    # Random walk: small daily moves around 0
    prices = 100 * np.cumprod(1 + np.random.normal(0, 0.01, len(dates)))
    return pd.DataFrame({"Date": dates, "ticker": "TEST", "Close": prices})


def test_var_is_negative(known_returns_df):
    """VaR represents a loss, so it should be negative."""
    result = compute_var(known_returns_df, confidence=0.95)
    assert result["VaR_pct"].iloc[0] < 0


def test_cvar_worse_than_var(known_returns_df):
    """CVaR (avg of the tail) must be <= VaR (the threshold) — it's the worse number."""
    result = compute_var(known_returns_df, confidence=0.95)
    assert result["CVaR_pct"].iloc[0] <= result["VaR_pct"].iloc[0]


def test_higher_confidence_means_larger_loss(known_returns_df):
    """99% VaR should predict a bigger loss than 95% VaR (further into the tail)."""
    var_95 = compute_var(known_returns_df, confidence=0.95)["VaR_pct"].iloc[0]
    var_99 = compute_var(known_returns_df, confidence=0.99)["VaR_pct"].iloc[0]
    assert var_99 <= var_95   # more negative = bigger loss


def test_dollar_var_scales_with_position():
    """$20k position should have exactly double the dollar VaR of $10k."""
    assert dollar_var(-0.02, 20000) == 2 * dollar_var(-0.02, 10000)


def test_dollar_var_sign():
    """A negative VaR % on a positive position = a negative dollar loss."""
    assert dollar_var(-0.02, 10000) < 0