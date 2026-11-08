"""The same SPY download, predictors, and target used in Weeks 4–8."""

import numpy as np
import pandas as pd
import yfinance as yf


START_DATE = "2020-01-01"
DEVELOPMENT_END = "2026-01-01"  # yfinance excludes the end date.
FEATURES = ["daily_return", "average_return_5d", "volatility_20d"]
EVALUATION_YEARS = [2024, 2025]


def download_spy(start=START_DATE, end=DEVELOPMENT_END):
    """Download public adjusted daily closes; defaults include only 2020–2025."""
    try:
        data = yf.download(
            "SPY", start=start, end=end, interval="1d",
            auto_adjust=True, multi_level_index=False, progress=False
        )
    except Exception as error:
        raise RuntimeError("SPY download failed. Check the internet connection and try again.") from error

    if data is None or data.empty:
        raise ValueError("No SPY data was downloaded. Check the connection and try again.")

    return data[["Close"]].sort_index()


def create_features(prices):
    """Keep the three original predictors, with every window ending today."""
    data = prices[["Close"]].dropna().sort_index().copy()
    returns = data["Close"].pct_change(fill_method=None)

    data["daily_return"] = returns
    data["average_return_5d"] = returns.rolling(5).mean()
    data["volatility_20d"] = returns.rolling(20).std()
    return data


def create_target(feature_data):
    """Add the next trading day's label using the fixed 2020–2023 cutoff rule."""
    data = feature_data.copy()
    rolling_volatility = data["volatility_20d"].dropna()
    cutoff = rolling_volatility.loc[:"2023"].quantile(0.75)
    if pd.isna(cutoff):
        raise ValueError("The target needs historical volatility values from 2020–2023.")

    high_volatility = (rolling_volatility > cutoff).astype(int)
    target = high_volatility.shift(-1).dropna().astype(int)
    data["target"] = target
    data["target_date"] = data.index.to_series().shift(-1)
    data[FEATURES] = data[FEATURES].replace([np.inf, -np.inf], np.nan)

    # Keep incomplete rows here so the notebooks can show them before removal.
    return data, cutoff
