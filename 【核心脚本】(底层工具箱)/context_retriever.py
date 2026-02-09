#!/usr/bin/env python3
"""
Context Retriever - 跨部门联想引擎
自动检索历史金融研报，为代码任务提供上下文
"""

from pathlib import Path
from datetime import datetime, timedelta
import json

def get_recent_reports(days=7):
    """
    获取最近 N 天的报告摘要

    Args:
        days: 回溯天数

    Returns:
        list: 报告摘要列表
    """
    reports_dir = Path(__file__).parent.parent / "【金融汇报】(分析主理人)" / "今日报告"

    if not reports_dir.exists():
        return []

    recent_files = sorted(reports_dir.glob("*.md"), key=lambda x: x.stat().st_mtime)[-days:]

    summaries = []
    for f in recent_files:
        try:
            content = f.read_text(encoding='utf-8')
            # 提取关键决策（最后 500 字符通常包含结论）
            summary = {
                "date": f.stem,
                "file": str(f),
                "decision": content[-500:] if len(content) > 500 else content
            }
            summaries.append(summary)
        except Exception as e:
            print(f"⚠️ 读取 {f.name} 失败: {e}")

    return summaries

def search_related_context(keyword):
    """
    根据关键词搜索相关历史分析

    Args:
        keyword: 搜索关键词（如 "BTC", "止损", "FOMO"）

    Returns:
        list: 相关报告片段
    """
    reports = get_recent_reports(days=30)
    matches = []

    for report in reports:
        if keyword.lower() in report["decision"].lower():
            matches.append({
                "date": report["date"],
                "snippet": report["decision"][:200]
            })

    return matches

if __name__ == "__main__":
    print("🔍 跨部门联想引擎测试\n")

    # 测试 1: 获取最近 7 天报告
    recent = get_recent_reports(7)
    print(f"✅ 最近 7 天报告数量: {len(recent)}")

    # 测试 2: 搜索关键词
    btc_context = search_related_context("BTC")
    print(f"✅ 包含 'BTC' 的历史分析: {len(btc_context)} 条")

    if btc_context:
        print(f"\n最新相关分析 ({btc_context[0]['date']}):")
        print(btc_context[0]['snippet'])
