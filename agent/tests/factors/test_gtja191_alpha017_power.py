"""GTJA #17 raises the percentile rank to the signed 5-day close change.

A rank of 0.5 and a close change of -2 is 0.5 ** -2 = 4. Taking the absolute
value of the exponent reported 0.25.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.factors.zoo.gtja191 import alpha_017


def test_negative_close_change_inverts_the_rank_power():
    idx = pd.bdate_range("2024-01-01", periods=20)
    close = pd.DataFrame(10.0, index=idx, columns=["A", "B"])
    close.iloc[-1] = [8.0, 12.0]
    vwap = pd.DataFrame(10.0, index=idx, columns=["A", "B"])
    vwap.iloc[-1] = [8.0, 10.0]
    panel = {
        "close": close,
        "vwap": vwap,
        "volume": pd.DataFrame(1.0, index=idx, columns=["A", "B"]),
        "amount": pd.DataFrame(1.0, index=idx, columns=["A", "B"]),
    }

    got = alpha_017.compute(panel).iloc[-1]

    # vwap - 15-day max is -2 and 0, so the percentile ranks are 0.5 and 1.
    # Deltas are -2 and +2.
    assert got["A"] == 4.0
    assert got["B"] == 1.0
    assert not np.isclose(got["A"], 0.25)
