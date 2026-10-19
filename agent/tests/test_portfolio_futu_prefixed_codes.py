"""Futu's market-prefixed codes must reach the risk x-ray and merge across brokers."""

from __future__ import annotations

from src.portfolio.normalization import normalize_position
from src.portfolio.service import PortfolioService


def _futu(code: str, market: str, currency: str) -> dict:
    position = normalize_position(
        "futu",
        {"code": code, "qty": 10, "market_val": 1000, "average_cost": 90,
         "market": market, "currency": currency},
    )
    position.update(priced=True, market_value_usd=1000, broker="futu")
    return position


def test_futu_prefixed_codes_are_risk_xray_symbols() -> None:
    args = PortfolioService._risk_xray_args(
        [_futu("HK.00700", "HK", "HKD"), _futu("US.AAPL", "US", "USD")]
    )
    assert sorted(args["symbols"]) == ["00700.HK", "AAPL.US"]


def test_futu_and_suffix_form_holdings_merge() -> None:
    longbridge = {"symbol": "700.HK", "currency": "HKD", "market": "HK", "broker": "longbridge",
                  "asset_type": "stock", "market_value_usd": 500}
    ibkr = {"symbol": "AAPL", "currency": "USD", "market": "US", "broker": "ibkr",
            "asset_type": "stock", "market_value_usd": 300}
    rows = PortfolioService._combine_holdings(
        [_futu("HK.00700", "HK", "HKD"), longbridge, _futu("US.AAPL", "US", "USD"), ibkr]
    )
    by_id = {row["canonical_id"]: row for row in rows}
    assert set(by_id) == {"HK:700", "US:AAPL"}
    assert by_id["HK:700"]["duplicate_across_brokers"] is True
    assert by_id["HK:700"]["brokers"] == ["futu", "longbridge"]
    assert by_id["US:AAPL"]["brokers"] == ["futu", "ibkr"]



def test_suffix_form_symbols_still_route_to_the_risk_xray() -> None:
    position = {"symbol": "700.HK", "currency": "HKD", "market": "HK", "priced": True,
                "market_value_usd": 1000, "asset_type": "stock"}
    assert PortfolioService._risk_xray_symbol(position) == "700.HK"
