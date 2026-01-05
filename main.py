import time
from datetime import datetime, timezone
from universe import get_top10_futures_symbols
from orb_engine import get_daily_orb, check_breakout
from notifier import send_telegram
from config import BINANCE_FAPI
import requests

SYMBOLS = []
ALERTED = {}
LAST_REFRESH = 0

def main():
    global SYMBOLS, LAST_REFRESH, ALERTED
    print("ORB Scanner starting...")

    SYMBOLS = get_top10_futures_symbols()
    print(f"Scanning: {SYMBOLS}")
    LAST_REFRESH = time.time()

    while True:
        try:
            current_time = time.time()

            if current_time - LAST_REFRESH > 14400:
                SYMBOLS = get_top10_futures_symbols()
                print(f"Refreshed symbols: {SYMBOLS}")
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
                            print(f"Alert sent: {symbol} {direction} at {close}")

                except Exception as e:
                    print(f"Error processing {symbol}: {e}")
                    continue

            time.sleep(30)

        except KeyboardInterrupt:
            print("\nShutting down...")
            break
        except Exception as e:
            print(f"Main loop error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
