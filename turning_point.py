"""Turning point detection for macro trends."""
from __future__ import annotations

from typing import Dict, List


def _window_slope(values: List[float]) -> float:
    if len(values) < 2:
        return 0.0
    return (values[-1] - values[0]) / (len(values) - 1)


def detect_turning_point(values: List[float], short_window: int = 3, long_window: int = 6) -> Dict[str, object]:
    """Detect trend change by comparing short/long window slopes."""
    if len(values) < long_window:
        return {"拐点信号": "样本不足", "拐点概率": 0.0, "方向": "未知"}

    short_values = values[-short_window:]
    long_values = values[-long_window:]

    short_slope = _window_slope(short_values)
    long_slope = _window_slope(long_values)

    divergence = abs(short_slope - long_slope)
    raw_prob = min(1.0, divergence * 8)

    if long_slope > 0 and short_slope < 0:
        signal = "出现下行拐点"
        direction = "向下"
        prob = min(1.0, raw_prob + 0.2)
    elif long_slope < 0 and short_slope > 0:
        signal = "出现上行拐点"
        direction = "向上"
        prob = min(1.0, raw_prob + 0.2)
    else:
        signal = "未出现显著拐点"
        direction = "延续"
        prob = raw_prob * 0.5

    return {
        "拐点信号": signal,
        "拐点概率": round(prob, 2),
        "方向": direction,
        "短期斜率": round(short_slope, 4),
        "中期斜率": round(long_slope, 4),
    }
