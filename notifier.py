import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram(symbol, direction, close_price, or_level, timestamp):
    msg = f"""*ORB Breakout: {symbol}*
Direction: {direction}
Close: `{close_price:.4f}`
OR {direction}: `{or_level:.4f}`
Time: {timestamp} UTC"""
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    requests.get(url, params=params, timeout=10)
