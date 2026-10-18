"""Sub-penny assets must not have their Bollinger/MACD output rounded to zero."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.tools.technical_indicator_tool import _compute_bollinger, _compute_macd


def _series(scale: float) -> pd.Series:
    rng = np.random.RandomState(0)
    return pd.Series(scale * np.cumprod(1 + rng.normal(0, 0.02, 80)))


def test_bollinger_keeps_precision_for_sub_penny_price() -> None:
    bands = _compute_bollinger(_series(1.2e-5))
    assert bands is not None
    assert bands["lower"] > 0
    assert bands["lower"] < bands["middle"] < bands["upper"]


def test_macd_keeps_precision_for_sub_penny_price() -> None:
    macd = _compute_macd(_series(1.2e-5))
    assert macd is not None
    assert macd["macd_line"] != 0.0
    assert macd["signal_line"] != 0.0


def test_ordinary_price_rounding_is_unchanged() -> None:
    close = _series(150.0)
    bands = _compute_bollinger(close)
    macd = _compute_macd(close)
    assert bands is not None and macd is not None
    assert all(round(v, 2) == v for v in bands.values())
    assert all(round(v, 4) == v for v in macd.values())
