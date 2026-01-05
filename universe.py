import requests
from config import COINGECKO_URL, BINANCE_FAPI

def get_top10_futures_symbols():
    # Top 10 by volume from CoinGecko
    url = f"{COINGECKO_URL}/coins/markets"
    params = {"vs_currency": "usd", "order": "volume_desc", "per_page": "10", "page": "1"}
    coins = requests.get(url, params=params).json()
    
    # Get all Binance USDT-M futures symbols
    exchange_info = requests.get(f"{BINANCE_FAPI}/fapi/v1/exchangeInfo").json()
    futures_symbols = {s["symbol"] for s in exchange_info["symbols"] if s["status"] == "TRADING" and s["symbol"].endswith("USDT")}
    
    # Map CoinGecko to Binance futures
    symbols = []
    for coin in coins:
        symbol = coin["symbol"].upper() + "USDT"
        if symbol in futures_symbols:
            symbols.append(symbol)
    
    return symbols[:10]  # Max 10
