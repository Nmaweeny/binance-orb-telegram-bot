import time
from datetime import datetime, timezone
from flask import Flask
import threading
from universe import get_top10_futures_symbols
from orb_engine import get_daily_orb, check_breakout
from notifier import send_telegram
from config import BINANCE_FAPI
import requests

app = Flask(__name__)

SYMBOLS = []
ALERTED = {}
LAST_REFRESH = 0

@app.route('/')
def health():
    """Render health check"""
    return {"status": "running", "symbols": len(SYMBOLS)}, 200

def scanner_loop():
    global SYMBOLS, LAST_REFRESH, ALERTED
    print("🚀 ORB Scanner starting...")

    SYMBOLS = get_top10_futures_symbols()
    print(f"📊 Scanning: {SYMBOLS}")
    LAST_REFRESH = time.time()

    while True:
        try:
            current_time = time.time()

            if current_time - LAST_REFRESH > 14400:
                SYMBOLS = get_top10_futures_symbols()
                print(f"🔄 Refreshed symbols: {SYMBOLS}")
                LAST_REFRESH = current_time

            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            new_alerted = {k: v for k, v in ALERTED.items() if today in k}
            ALERTED = new_alerted

            for symbol in SYMBOLS:
                try:
                    url = f"{BINANCE_FAPI}/fapi/v1/klines"
                    params = {
                        "symbol": symbol,
                        "interval": "5m",
                        "limit": 2
                    }
                    response = requests.get(url, params=params, timeout=10)
                    klines = response.json()

                    if len(klines) < 2:
                        continue

                    latest_closed = klines[-2]

                    or_high, or_low = get_daily_orb(symbol)

                    if or_high is None or or_low is None:
                        continue

                    direction, close, level, ts = check_breakout(symbol, or_high, or_low, latest_closed)

                    if direction:
                        alert_key = f"{symbol}_{direction}_{today}"

                        if alert_key not in ALERTED:
                            send_telegram(symbol, direction, close, level, ts)
                            ALERTED[alert_key] = True
                            print(f"🚨 Alert: {symbol} {direction} @ {close}")

                except Exception as e:
                    print(f"Error processing {symbol}: {e}")
                    continue

            time.sleep(30)

        except KeyboardInterrupt:
            print("\n⏹️ Shutting down...")
            break
        except Exception as e:
            print(f"Main loop error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    # Start scanner in background thread
    scanner_thread = threading.Thread(target=scanner_loop, daemon=True)
    scanner_thread.start()
    
    # Flask binds to port 5000 (required by Render)
    app.run(host='0.0.0.0', port=5000, debug=False)
