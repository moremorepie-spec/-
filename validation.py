"""Market confirmation module."""
from __future__ import annotations

from typing import Dict, List


def _pct_change(values: List[float], lookback: int = 3) -> float:
    if len(values) <= lookback or values[-lookback - 1] == 0:
        return 0.0
    return (values[-1] - values[-lookback - 1]) / values[-lookback - 1]


def validate_macro_with_market(
    macro_state: str,
    equity_values: List[float],
    vix_values: List[float],
    bond_yield_values: List[float],
) -> Dict[str, str]:
    """Cross-check macro narrative with market behavior."""
    equity_ret = _pct_change(equity_values, lookback=3)
    vix_ret = _pct_change(vix_values, lookback=3)
    bond_move = _pct_change(bond_yield_values, lookback=3)

    risk_on = equity_ret > 0.01 and vix_ret < 0.03
    risk_off = equity_ret < -0.01 and vix_ret > 0.05

    if macro_state in {"增长修复", "宽松+去通胀"} and risk_on:
        market_validation = "已确认"
    elif macro_state in {"紧缩+再通胀", "滞胀/增长走弱"} and risk_off:
        market_validation = "已确认"
    else:
        market_validation = "待确认"

    if risk_off or vix_values[-1] > 24:
        risk_level = "高"
    elif risk_on and abs(bond_move) < 0.03:
        risk_level = "中低"
    else:
        risk_level = "中"

    return {
        "市场验证": market_validation,
        "风险等级": risk_level,
        "股市3个月涨跌": f"{equity_ret:.2%}",
        "VIX3个月变化": f"{vix_ret:.2%}",
        "10Y收益率3个月变化": f"{bond_move:.2%}",
    }


def generate_trade_suggestion(macro_state: str, turning_signal: str, risk_level: str) -> Dict[str, str]:
    """Generate high-level cross-asset positioning ideas."""
    if risk_level == "高":
        return {
            "股票": "降低仓位，偏防御板块",
            "债券": "增配中高评级债券",
            "商品": "降低高波动商品敞口",
            "外汇": "偏好避险货币",
        }

    if macro_state == "增长修复":
        return {
            "股票": "增配顺周期与成长",
            "债券": "中性久期",
            "商品": "关注工业品与能源",
            "外汇": "偏多高贝塔货币",
        }

    if macro_state == "宽松+去通胀":
        return {
            "股票": "均衡配置，偏好高现金流资产",
            "债券": "适度拉长久期",
            "商品": "中性，回避过热品种",
            "外汇": "关注套息策略",
        }

    if "下行拐点" in turning_signal:
        return {
            "股票": "逐步降低风险资产仓位",
            "债券": "提高利率债配置",
            "商品": "降低周期品",
            "外汇": "偏多美元或避险货币",
        }

    return {
        "股票": "中性偏防御",
        "债券": "中性久期",
        "商品": "控制仓位",
        "外汇": "保持分散",
    }
