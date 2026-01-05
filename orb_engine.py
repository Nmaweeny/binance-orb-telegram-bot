import requests
from datetime import datetime, timezone
from config import BINANCE_FAPI

def get_daily_orb(symbol):
    """Get OR high/low from first 5m candle of UTC day"""
    now = datetime.now(timezone.utc)
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    url = f"{BINANCE_FAPI}/fapi/v1/klines"
    params = {"symbol": symbol, "interval": "5m", "limit": 288}  # ~1 day
    klines = requests.get(url, params=params).json()
    
    # Find first candle of today (index 0 if new day)
    first_candle = klines[0]
    return float(first_candle[2]), float(first_candle[3])  # high, low

def check_breakout(symbol, or_high, or_low, latest_klines):
    """Check if latest closed candle broke OR"""
    latest = latest_klines[-1]  # Last completed candle
    close = float(latest[4])
    timestamp = datetime.fromtimestamp(latest[0]/1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
    
    if close > or_high:
        return "BULL", close, or_high, timestamp
    if close < or_low:
        return "BEAR", close, or_low, timestamp
    return None, None, None, None
