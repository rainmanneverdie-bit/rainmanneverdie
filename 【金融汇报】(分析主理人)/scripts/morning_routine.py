#!/usr/bin/env python3
"""
Morning Routine Entry Point
早间任务主入口 - 每天 8:00 AM 自动触发
"""

import sys
import os
from pathlib import Path

# 添加当前目录到路径
curr_dir = Path(__file__).parent
sys.path.append(str(curr_dir))

from trader_agent import WallStreetTrader
from wechat_pusher import push_to_wechat

def start_morning_routine():
    print("🌅 开启早间华尔街交易员模式...")
    
    # 1. 运行专业交易员 Agent 生成报告
    trader = WallStreetTrader()
    report_content = trader.generate_daily_report()
    
    # 2. 推送至微信
    push_to_wechat("📊 今日华尔街交易指令", report_content)

if __name__ == "__main__":
    start_morning_routine()
