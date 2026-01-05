# ORB Scanner - Opening Range Breakout Bot

A 24/7 automated scanner that monitors the top 10 Binance USDT perpetual futures pairs and sends Telegram notifications when price breaks out of the daily opening range.

## Features

- Tracks top 10 coins by 24h trading volume on Binance Futures
- Monitors Opening Range (first 5-minute candle of each UTC day)
- Real-time breakout detection (bull and bear)
- Telegram notifications for all breakouts
- Automatic symbol refresh every 4 hours
- Daily alert reset to avoid duplicates

## How It Works

1. At the start of each UTC day (00:00), the scanner records the high and low of the first 5-minute candle as the Opening Range
2. Every 30 seconds, it checks if any 5-minute candle closed above the OR high (bull breakout) or below the OR low (bear breakout)
3. When a breakout occurs, you receive a Telegram alert with the symbol, direction, close price, and timestamp
4. Only one alert per symbol per direction per day to avoid spam

## Setup

### 1. Get Telegram Bot Token

- Open Telegram and search for @BotFather
- Send `/newbot` and follow the instructions
- Save your bot token

### 2. Get Your Telegram Chat ID

- Search for @userinfobot on Telegram
- Start the bot and it will show your chat ID
- Save this number

### 3. Configure Environment Variables

Copy the example file and add your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Scanner

```bash
python main.py
```

## Deployment

The scanner is configured for deployment on Render.com using the included `render.yaml` file.

1. Push your code to a Git repository
2. Create a new Web Service on Render
3. Connect your repository
4. Add environment variables in Render dashboard
5. Deploy

## Project Structure

- `main.py` - Main loop that coordinates scanning
- `universe.py` - Fetches top 10 symbols by volume
- `orb_engine.py` - Calculates opening range and detects breakouts
- `notifier.py` - Sends Telegram notifications
- `config.py` - Configuration and environment variables
- `requirements.txt` - Python dependencies

## Alert Format

```
ORB Breakout: BTCUSDT
Direction: BULL
Close: 45123.4500
OR BULL: 45000.0000
Time: 2026-01-05 14:35 UTC
```

## Notes

- The scanner runs continuously and will restart automatically on errors
- Symbol list refreshes every 4 hours to track the most active markets
- All times are in UTC
- Opening range resets daily at 00:00 UTC
