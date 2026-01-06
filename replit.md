# ORB Scanner - Opening Range Breakout Bot

## Overview

A 24/7 automated scanner that monitors the top 10 Binance USDT perpetual futures pairs and sends Telegram notifications when price breaks out of the daily opening range.

## Project Structure

- `main.py` - Main Flask app and scanner loop coordinator
- `universe.py` - Fetches top 10 symbols by volume from Binance
- `orb_engine.py` - Calculates opening range and detects breakouts
- `notifier.py` - Sends Telegram notifications
- `config.py` - Configuration and environment variables

## Tech Stack

- Python 3.11
- Flask (web server for health checks)
- Requests (API calls to Binance and Telegram)
- python-dotenv (environment variable management)

## Environment Variables

The following secrets are required for full functionality:
- `TELEGRAM_BOT_TOKEN` - Telegram bot token from @BotFather
- `TELEGRAM_CHAT_ID` - Your Telegram chat ID

The app will run without these but Telegram notifications will be disabled.

## How It Works

1. Monitors the first 5-minute candle of each UTC day as the Opening Range
2. Every 30 seconds, checks if any candle closes above OR high (bull) or below OR low (bear)
3. Sends Telegram alerts on breakouts (one per symbol per direction per day)
4. Symbol list refreshes every 4 hours

## Deployment

- Uses VM deployment (always running) since this is a continuous background scanner
- Health check endpoint available at `/`
