# AI宏观分析系统

一个可扩展的 Python 宏观分析项目，用于每日自动分析宏观数据，输出宏观状态、拐点信号与跨资产交易建议。

## 项目结构

```text
.
├── data_loader.py      # 数据模块：支持 mock 与 API（占位）
├── macro_agent.py      # 宏观 Agent：利率/通胀/周期分析
├── turning_point.py    # 拐点检测：3个月趋势变化检测
├── validation.py       # 市场验证：股市/VIX/债券确认逻辑
├── main.py             # 主程序：整合并输出 JSON
└── README.md
```

## 功能说明

- **数据模块**：
  - `load_macro_data(source="mock"|"api")`
  - 内置模拟数据包含：利率、CPI、PMI、VIX、美元指数，以及市场验证所需的股指与10Y收益率。
- **宏观Agent**：
  - `analyze_rate_trend`
  - `analyze_inflation_trend`
  - `analyze_business_cycle`
  - `synthesize_macro_state`
- **拐点检测模块**：
  - `detect_turning_point(values, short_window=3, long_window=6)`
- **市场验证模块**：
  - `validate_macro_with_market`
  - `generate_trade_suggestion`
- **主程序**：
  - `run_macro_pipeline`
  - CLI 输出标准 JSON。

## 运行方式

```bash
python main.py
```

可选参数：

```bash
python main.py --source mock --months 12
```

> 若使用 `--source api`，请先在 `data_loader.py` 中实现 `_load_from_api()`。

## 输出示例

```json
{
  "宏观状态": "增长修复",
  "阶段": "复苏",
  "拐点信号": "未出现显著拐点",
  "拐点概率": 0.19,
  "市场验证": "已确认",
  "风险等级": "中低",
  "交易建议": {
    "股票": "增配顺周期与成长",
    "债券": "中性久期",
    "商品": "关注工业品与能源",
    "外汇": "偏多高贝塔货币"
  }
}
```

## 扩展建议

1. 接入 FRED / Wind / Bloomberg / TradingEconomics API。
2. 将拐点检测升级为统计检验（结构突变、HMM、贝叶斯切换模型）。
3. 增加日志、告警、定时任务（cron/Airflow）。
4. 将规则引擎替换为模型推断（LLM + 因子模型）。
