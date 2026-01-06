import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram(symbol, direction, close_price, or_level, timestamp):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"[Telegram disabled] Would send alert: {symbol} {direction} @ {close_price:.4f}")
        return
    
    chart_url = f"https://www.binance.com/en/futures/{symbol}"
    msg = f"""*ORB Breakout: {symbol}*
Direction: {direction}
Close: `{close_price:.4f}`
OR {direction}: `{or_level:.4f}`
Time: {timestamp} UTC

[📊 View Chart]({chart_url})"""
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    requests.get(url, params=params, timeout=10)
