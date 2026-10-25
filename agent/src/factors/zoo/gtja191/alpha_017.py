
# ============================================================
# 中文名称: GTJA #17 - 价格振幅比
# 简要说明: RANK(DELTA(VWAP, 1))^3 / RANK(CORR(LOW, MEAN(VOLUME,50), 12))，VWAP变化与量价相关的比率。
# 典型用途: VWAP变化速度相对于成交量-价格关系的归一化指标。
# ============================================================
"""GTJA Alpha #17.

Formula: (RANK(VWAP - MAX(VWAP,15))^DELTA(CLOSE,5))
Source: 国泰君安 191 alpha 研报 (2014), alpha 17."""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.factors.base import (
    decay_linear,
    delta,
    rank,
    safe_div,
    signed_power,
    ts_argmax,
    ts_argmin,
    ts_corr,
    ts_cov,
    ts_max,
    ts_mean,
    ts_min,
    ts_rank,
    ts_std,
    vwap,
)

__alpha_meta__ = {
    "id": "gtja191_017",
    "theme": ['reversal'],
    "formula_latex": '(RANK(VWAP - MAX(VWAP,15))^DELTA(CLOSE,5))',
    "columns_required": ['close', 'volume', 'amount'],
    "extras_required": [],
    "requires_sector": False,
    "universe": ["equity_cn"],
    "frequency": ["1d"],
    "decay_horizon": 15,
    "min_warmup_bars": 16,
    "notes": 'The base is a percentile rank in (0, 1], so a negative 5-day close change is a real power, not a complex one.',
}

def compute(panel: dict) -> pd.DataFrame:
    c = panel["close"]
    v = panel["volume"]
    vw = vwap(panel, "equity_cn")
    base = rank(vw - ts_max(vw, 15))
    expo = delta(c, 5)
    # rank() is a percentile in (0, 1], so the report's power is real even when
    # the 5-day close change is negative. Dropping the sign of that change
    # turned 0.5 ** -2 into 0.25 instead of 4.
    out_arr = np.power(
        base.to_numpy(dtype=float, na_value=np.nan),
        expo.to_numpy(dtype=float, na_value=np.nan),
    )
    return pd.DataFrame(out_arr, index=c.index, columns=c.columns)
