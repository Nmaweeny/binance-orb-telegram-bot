import requests
from config import BINANCE_FAPI

def get_top10_futures_symbols():
    try:
        url = f"{BINANCE_FAPI}/fapi/v1/ticker/24hr"
        response = requests.get(url, timeout=10)
        tickers = response.json()

        usdt_pairs = [
            ticker for ticker in tickers
            if ticker["symbol"].endswith("USDT")
        ]

        sorted_pairs = sorted(
            usdt_pairs,
            key=lambda x: float(x["quoteVolume"]),
            reverse=True
        )

        top10 = [pair["symbol"] for pair in sorted_pairs[:10]]

        return top10

    except Exception as e:
        print(f"Error fetching top symbols: {e}")
        return ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
