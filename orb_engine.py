import requests
from datetime import datetime, timezone
from config import BINANCE_FAPI

ORB_CACHE = {}

def get_daily_orb(symbol):
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")

    cache_key = f"{symbol}_{today}"
    if cache_key in ORB_CACHE:
        return ORB_CACHE[cache_key]

    day_start_ts = int(now.replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000)

    url = f"{BINANCE_FAPI}/fapi/v1/klines"
    params = {
        "symbol": symbol,
        "interval": "5m",
        "startTime": day_start_ts,
        "limit": 1
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        klines = response.json()

        if not klines or len(klines) == 0:
            return None, None

        first_candle = klines[0]
        or_high = float(first_candle[2])
        or_low = float(first_candle[3])

        ORB_CACHE[cache_key] = (or_high, or_low)

        return or_high, or_low

    except Exception as e:
        print(f"Error fetching ORB for {symbol}: {e}")
        return None, None

def check_breakout(symbol, or_high, or_low, latest_candle):
    if or_high is None or or_low is None:
        return None, None, None, None

    close = float(latest_candle[4])
    timestamp = datetime.fromtimestamp(latest_candle[0]/1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")

    if close > or_high:
        return "BULL", close, or_high, timestamp
    if close < or_low:
        return "BEAR", close, or_low, timestamp

    return None, None, None, None
