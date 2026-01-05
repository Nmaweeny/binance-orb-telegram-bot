import time
from universe import get_top10_futures_symbols
from orb_engine import get_daily_orb, check_breakout
from notifier import send_telegram
from config import BINANCE_FAPI
import requests

SYMBOLS = []
ALERTED = {}  # symbol -> last alerted timestamp

def main():
    global SYMBOLS
    print("🚀 ORB Scanner starting...")
    
    while True:
        try:
            # Refresh universe every 4 hours
            if time.time() % 14400 < 300:
                SYMBOLS = get_top10_futures_symbols()
                print(f"📊 Scanning: {SYMBOLS}")
            
            for symbol in SYMBOLS:
                klines = requests.get(f"{BINANCE_FAPI}/fapi/v1/klines", 
                                    params={"symbol": symbol, "interval": "5m", "limit": 3}).json()
                
                or_high, or_low = get_daily_orb(symbol)
                direction, close, level, ts = check_breakout(symbol, or_high, or_low, klines)
                
                key = f"{symbol}_{direction}_{ts}"
                if direction and key not in ALERTED:
                    send_telegram(symbol, direction, close, level, ts)
                    ALERTED[key] = True
                    print(f"🚨 Alert: {symbol} {direction}")
            
            time.sleep(30)  # Poll every 30s
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
