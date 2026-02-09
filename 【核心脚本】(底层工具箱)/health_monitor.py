#!/usr/bin/env python3
"""
Health Monitor - 系统健康检查
每小时检查关键服务状态，异常时推送告警
"""

import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def check_deepseek_api():
    """检查 DeepSeek API"""
    try:
        from agno.models.deepseek import DeepSeek
        model = DeepSeek(id="deepseek-chat")
        return {"status": "✅", "service": "DeepSeek API"}
    except Exception as e:
        return {"status": "❌", "service": "DeepSeek API", "error": str(e)}

def check_ccxt():
    """检查 CCXT 交易所连接"""
    try:
        import ccxt
        exchange = ccxt.okx()
        ticker = exchange.fetch_ticker('BTC/USDT')
        return {"status": "✅", "service": "CCXT (OKX)", "price": ticker['last']}
    except Exception as e:
        return {"status": "❌", "service": "CCXT (OKX)", "error": str(e)}

def check_pushplus():
    """检查 PushPlus 推送服务"""
    token = os.getenv("PUSHPLUS_TOKEN")
    if not token:
        return {"status": "⚠️", "service": "PushPlus", "error": "Token 未配置"}

    try:
        url = "http://www.pushplus.plus/send"
        data = {"token": token, "title": "健康检查", "content": "系统正常", "template": "txt"}
        response = requests.post(url, json=data, timeout=5)
        result = response.json()

        if result.get("code") == 200:
            return {"status": "✅", "service": "PushPlus"}
        else:
            return {"status": "❌", "service": "PushPlus", "error": result.get("msg")}
    except Exception as e:
        return {"status": "❌", "service": "PushPlus", "error": str(e)}

def check_github_token():
    """检查 GitHub Token"""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return {"status": "⚠️", "service": "GitHub Token", "error": "Token 未配置"}

    try:
        headers = {"Authorization": f"token {token}"}
        response = requests.get("https://api.github.com/user", headers=headers, timeout=5)

        if response.status_code == 200:
            user = response.json().get("login")
            return {"status": "✅", "service": "GitHub Token", "user": user}
        else:
            return {"status": "❌", "service": "GitHub Token", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "❌", "service": "GitHub Token", "error": str(e)}

def run_health_check():
    """执行完整健康检查"""
    print(f"🏥 系统健康检查 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    checks = [
        check_deepseek_api(),
        check_ccxt(),
        check_pushplus(),
        check_github_token()
    ]

    all_healthy = True
    for check in checks:
        status = check["status"]
        service = check["service"]

        if status == "✅":
            extra = f" (价格: ${check['price']})" if 'price' in check else ""
            extra += f" (用户: {check['user']})" if 'user' in check else ""
            print(f"{status} {service}{extra}")
        else:
            print(f"{status} {service}: {check.get('error', '未知错误')}")
            all_healthy = False

    print(f"\n{'✅ 所有服务正常' if all_healthy else '⚠️ 部分服务异常'}")
    return all_healthy

if __name__ == "__main__":
    run_health_check()
