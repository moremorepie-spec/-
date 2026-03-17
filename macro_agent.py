"""Macro agent logic for trend and regime analysis."""
from __future__ import annotations

from typing import Dict, List

from data_loader import MacroSeries


def _slope(values: List[float]) -> float:
    """Simple slope proxy: end minus start normalized by length."""
    if len(values) < 2:
        return 0.0
    return (values[-1] - values[0]) / (len(values) - 1)


def _trend_label(values: List[float], threshold: float) -> str:
    s = _slope(values)
    if s > threshold:
        return "上行"
    if s < -threshold:
        return "下行"
    return "震荡"


def analyze_rate_trend(rate_series: MacroSeries) -> Dict[str, object]:
    trend = _trend_label(rate_series.values[-6:], threshold=0.03)
    return {
        "趋势": trend,
        "当前值": rate_series.values[-1],
        "6个月斜率": round(_slope(rate_series.values[-6:]), 4),
    }


def analyze_inflation_trend(cpi_series: MacroSeries) -> Dict[str, object]:
    trend = _trend_label(cpi_series.values[-6:], threshold=0.02)
    return {
        "趋势": trend,
        "当前值": cpi_series.values[-1],
        "6个月斜率": round(_slope(cpi_series.values[-6:]), 4),
    }


def analyze_business_cycle(pmi_series: MacroSeries) -> Dict[str, str]:
    latest = pmi_series.values[-1]
    pmi_trend = _trend_label(pmi_series.values[-6:], threshold=0.08)

    if latest >= 50 and pmi_trend == "上行":
        phase = "复苏"
    elif latest >= 50 and pmi_trend in {"震荡", "下行"}:
        phase = "过热后放缓"
    elif latest < 50 and pmi_trend == "上行":
        phase = "衰退后修复"
    else:
        phase = "下行/衰退"

    return {"阶段": phase, "PMI趋势": pmi_trend}


def synthesize_macro_state(rate_info: Dict[str, object], inflation_info: Dict[str, object], cycle_info: Dict[str, str]) -> Dict[str, str]:
    r = rate_info["趋势"]
    i = inflation_info["趋势"]
    phase = cycle_info["阶段"]

    if r == "上行" and i == "上行":
        state = "紧缩+再通胀"
    elif r in {"下行", "震荡"} and i == "下行":
        state = "宽松+去通胀"
    elif phase in {"复苏", "衰退后修复"}:
        state = "增长修复"
    else:
        state = "滞胀/增长走弱"

    return {"宏观状态": state, "阶段": phase}
