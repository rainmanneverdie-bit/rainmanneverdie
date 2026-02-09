import pandas as pd
import numpy as np
import ccxt
from datetime import datetime

class LightweightSuperTA:
    """
    [REFACTORED INTEL] 针对 Python 3.14.2 环境优化的轻量级指标引擎。
    跳过 pandas-ta 的复杂依赖（numba），直接实现核心博弈指标。
    """
    def __init__(self, symbol='ETH/USDT', timeframe='1h'):
        self.symbol = symbol
        self.timeframe = timeframe
        self.exchange = ccxt.okx()

    def fetch_ohlcv(self, limit=100):
        print(f"📥 正在获取 {self.symbol} 数据...")
        ohlcv = self.exchange.fetch_ohlcv(self.symbol, self.timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    def calculate_rsi(self, series, period=14):
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def calculate_supertrend(self, df, period=10, multiplier=3):
        """
        手动实现超级趋势逻辑 (ATR Based)
        """
        hl2 = (df['high'] + df['low']) / 2
        # 简化版 ATR
        df['tr'] = np.maximum(df['high'] - df['low'], 
                             np.maximum(abs(df['high'] - df['close'].shift(1)), 
                                      abs(df['low'] - df['close'].shift(1))))
        atr = df['tr'].rolling(window=period).mean()
        
        df['upperband'] = hl2 + (multiplier * atr)
        df['lowerband'] = hl2 - (multiplier * atr)
        df['in_uptrend'] = True

        for i in range(1, len(df.index)):
            if df['close'][i] > df['upperband'][i-1]:
                df.loc[i, 'in_uptrend'] = True
            elif df['close'][i] < df['lowerband'][i-1]:
                df.loc[i, 'in_uptrend'] = False
            else:
                df.loc[i, 'in_uptrend'] = df['in_uptrend'][i-1]
                if df['in_uptrend'][i] and df['lowerband'][i] < df['lowerband'][i-1]:
                    df.loc[i, 'lowerband'] = df['lowerband'][i-1]
                if not df['in_uptrend'][i] and df['upperband'][i] > df['upperband'][i-1]:
                    df.loc[i, 'upperband'] = df['upperband'][i-1]
        return df

    def get_market_sentiment(self):
        df = self.fetch_ohlcv()
        df['rsi'] = self.calculate_rsi(df['close'])
        df = self.calculate_supertrend(df)
        
        last_row = df.iloc[-1]
        rsi_val = last_row['rsi']
        in_uptrend = last_row['in_uptrend']
        
        sentiment = "NEUTRAL"
        signal = "WAIT"
        
        if in_uptrend and rsi_val < 70:
            sentiment = "BULLISH"
            signal = "BUY/LONG"
        elif not in_uptrend and rsi_val > 30:
            sentiment = "BEARISH"
            signal = "SELL/SHORT"
            
        return {
            "symbol": self.symbol,
            "price": last_row['close'],
            "sentiment": sentiment,
            "signal": signal,
            "rsi": rsi_val,
            "supertrend": "UP" if in_uptrend else "DOWN",
            "timestamp": last_row['datetime'].strftime('%Y-%m-%d %H:%M:%S')
        }

if __name__ == "__main__":
    try:
        engine = LightweightSuperTA()
        res = engine.get_market_sentiment()
        print("\n" + "="*50)
        print(f"💎 LIGHTWEIGHT TA 实时结果 ({res['symbol']})")
        print(f"价格: {res['price']} | 情绪: {res['sentiment']}")
        print(f"信号: {res['signal']} | RSI: {res['rsi']:.2f}")
        print(f"趋势: {res['supertrend']}")
        print("="*50)
    except Exception as e:
        print(f"❌ 运行失败: {str(e)}")
