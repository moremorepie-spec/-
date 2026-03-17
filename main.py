"""Main entry for AI macro analysis system."""
from __future__ import annotations

import argparse
import json
from typing import Any, Dict

from data_loader import load_macro_data
from macro_agent import (
    analyze_business_cycle,
    analyze_inflation_trend,
    analyze_rate_trend,
    synthesize_macro_state,
)
from turning_point import detect_turning_point
from validation import generate_trade_suggestion, validate_macro_with_market


def run_macro_pipeline(source: str = "mock", months: int = 12) -> Dict[str, Any]:
    data = load_macro_data(source=source, months=months)

    rate_info = analyze_rate_trend(data["interest_rate"])
    inflation_info = analyze_inflation_trend(data["cpi"])
    cycle_info = analyze_business_cycle(data["pmi"])

    macro_summary = synthesize_macro_state(rate_info, inflation_info, cycle_info)

    turning = detect_turning_point(data["pmi"].values, short_window=3, long_window=6)

    market_check = validate_macro_with_market(
        macro_state=macro_summary["宏观状态"],
        equity_values=data["equity_index"].values,
        vix_values=data["vix"].values,
        bond_yield_values=data["bond_yield_10y"].values,
    )

    trade_suggestion = generate_trade_suggestion(
        macro_state=macro_summary["宏观状态"],
        turning_signal=turning["拐点信号"],
        risk_level=market_check["风险等级"],
    )

    return {
        "宏观状态": macro_summary["宏观状态"],
        "阶段": macro_summary["阶段"],
        "拐点信号": turning["拐点信号"],
        "拐点概率": turning["拐点概率"],
        "市场验证": market_check["市场验证"],
        "风险等级": market_check["风险等级"],
        "交易建议": trade_suggestion,
        "诊断细节": {
            "利率分析": rate_info,
            "通胀分析": inflation_info,
            "周期分析": cycle_info,
            "拐点分析": turning,
            "市场验证分析": market_check,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="AI宏观分析系统")
    parser.add_argument("--source", choices=["mock", "api"], default="mock", help="数据来源")
    parser.add_argument("--months", type=int, default=12, help="回看月数")
    args = parser.parse_args()

    result = run_macro_pipeline(source=args.source, months=args.months)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
