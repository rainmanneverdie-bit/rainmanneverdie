# 📉 Crypto Trading & Risk Management Protocol

## 1. Data Cleaning & Integrity
- **Mandatory Sources**: Always prioritize Coinglass (Liquidation/Funding) and CCXT (Multi-timeframe TA) over generic news.
- **Verification**: If a price discrepancy > 1% exists between sources, report it as a "Data Conflict" before making a recommendation.

## 2. Reasoning Loop (The 3-Pillar Analysis)
- **Pillar 1: Sentiment**: Analyze Fear & Greed Index + Official news sentiment (Bloomberg/Reuters/CoinDesk).
- **Pillar 2: Liquidity**: Identify "Magnet Zones" on the Liquidation Heatmap.
- **Pillar 3: Technicals**: EMA cross-checks + RSI divergence on 4h and 1d timeframes.

## 3. Decision Matrix
- **Bullish Bias**: Price > 4h EMA20 AND Funding is Positive AND Major Short Liquidation occurring.
- **Bearish Bias**: Price < 4h EMA20 AND RSI < 30 on 1h (but > 30 on 1d).
- **Wait Signal**: Ambiguous news OR Funding Rate > 0.1% (Extreme Greed).

## 4. Output Formatting
- **Standard**: Use the [Header: 情报汇总] -> [Technical: 指标研判] -> [Execution: 交易员建议] structure.
- **Decision Clarity**: Must output either `[入场价格/止损止盈]` or `[建议观望]`.

## 5. Fallback Strategy (数据源容错)
- **Primary**: DuckDuckGo News Search
- **Secondary**: 缓存的最近 24h 新闻（如果 Primary 失败）
- **Tertiary**: 纯技术面分析 + 历史宏观背景推演（如果 Secondary 也失败）
- **原则**: 外部 API 失败不应导致系统崩溃，必须有降级方案

