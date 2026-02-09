#!/usr/bin/env python3
"""
Wall Street Day Trader Agent
专业华尔街日内交易员 - 负责市场深度资讯抓取与入场决策
"""

from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv
import os
import json
from datetime import datetime
from pathlib import Path

# 加载环境
load_dotenv()

# 设置路径
PROJECT_ROOT = Path(__file__).parent.parent
REPORTS_DIR = PROJECT_ROOT / "今日报告"

from data_engine import get_market_data, get_coinglass_summary
from wechat_pusher import send_wechat

class WallStreetTrader:
    def __init__(self):
        # 加载人设档案
        aboutme_path = PROJECT_ROOT / "Knowledge_Archive" / "aboutme.md"
        self.user_profile = ""
        if aboutme_path.exists():
            with open(aboutme_path, 'r', encoding='utf-8') as f:
                self.user_profile = f.read()

        # 优化: 包装工具以增强稳定性
        ddg_tool = DuckDuckGoTools()

        self.agent = Agent(
            name="WallStreet-Trader",
            model=DeepSeek(id="deepseek-chat"),
            tools=[ddg_tool],
            description="你是一名顶级华尔街日内交易员，受雇于 AlexWang。你的决策冷静、客观且极具前瞻性。",
            instructions=[
                "1. 核心任务：搜集过去 24h 对 BTC/ETH 产生重大影响的全球要闻（Bloomberg, Reuters, WSJ, CoinDesk 等）。",
                "2. 深度要求：每条新闻必须分析其对『流动性』或『情绪面』的具体影响，附带 [Source: URL]。",
                "3. 核心研判：结合系统提供的 CCXT 技术指标与 Coinglass 筹码数据进行三位一体分析。",
                "4. 风格对齐：高信息密度，直接点出『庄家意图』与『散户分布』，严禁使用『可能』、『或许』等含糊词汇。",
                "5. 确定性结论：给出绝对明确的入场建议：[入场价/止损止盈] 或 [今日建议等待]。",
                "6. 输出格式：Markdown 结构，严选头条，拒绝信息噪音。",
                "7. 反方博弈：在给出最终决策前，必须在 <thought> 标签中评估反方观点与潜在回撤风险。",
                "8. 人设对齐：严格遵守 AlexWang 的交易风格（单笔风险 2-5%、拒绝 FOMO、三位一体验证）。"
            ],
            markdown=True
        )

    def generate_daily_report(self):
        print("🚀 正在抓取情报与技术指标并生成决策分析...")
        today_str = datetime.now().strftime("%Y-%m-%d")

        try:
            # 获取真实市场数据
            market_stats = get_market_data()
            coinglass_stats = get_coinglass_summary()

            prompt = f"""
            今天是 {today_str}。

            【AlexWang 交易风格档案】:
            {self.user_profile}

            【市场实时数据】:
            - CCXT (15m/1h/4h/1d): {json.dumps(market_stats)}
            - Coinglass: {json.dumps(coinglass_stats)}

            执行任务：
            1. 搜索并汇总 5 条以上核心要闻。如果搜索无结果，请基于现有技术指标和筹码数据，结合历史宏观背景给出『黑天鹅』或『流动性枯竭』的压力测试分析。
            2. 在 <thought> 标签中进行反方博弈：评估多空双方观点，识别潜在回撤风险。
            3. 结合 AlexWang 的风险偏好（单笔 2-5%、拒绝 FOMO），给出终极决策。
            4. 如果建议入场，必须明确：入场价、止损位、止盈位、仓位比例。
            """

            response = self.agent.run(prompt)
            report_content = response.content

        except Exception as e:
            # 强化底层容错机制
            print(f"⚠️ 研报生成过程中遭遇非预期崩溃: {str(e)}")
            report_content = f"# 🚨 异常交易指令 (系统冗余模式)\n\n原因: 核心检索链路中断。建议查阅终端运行日志。"

        # 保存报告
        report_file = REPORTS_DIR / f"{today_str}.md"
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report_content)

        print(f"✅ 报告已生成至: {report_file}")
        if report_content:
            # 自动推送到微信
            print("📤 正在推送报告至微信...")
            push_title = f"📢 华尔街早报 ({today_str})"
            send_wechat(push_title, report_content)

        return report_content

if __name__ == "__main__":
    trader = WallStreetTrader()
    trader.generate_daily_report()
