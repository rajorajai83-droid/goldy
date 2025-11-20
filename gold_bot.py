# gold_bot.py
# Auto GOLD XAUUSD Forex Bot (SMA20 vs SMA50)
# VIP Style Signals + TP1..TP5 + SL + TradingView Chart Screenshot

import os
import telegram
import requests
import pandas as pd
from datetime import datetime
from chart import get_chart

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telegram.Bot(token=BOT_TOKEN)

# -----------------------------
# 📌 GET LIVE GOLD PRICE (FAST API)
# -----------------------------
def get_xauusd_price():
    url = "https://query1.finance.yahoo.com/v8/finance/chart/XAUUSD=X"
    data = requests.get(url).json()
    price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
    return float(price)

# -----------------------------
# 📌 GENERATE BUY/SELL SIGNAL USING SMA20 & SMA50
# -----------------------------
def generate_signal(df):
    df["sma20"] = df["close"].rolling(20).mean()
    df["sma50"] = df["close"].rolling(50).mean()

    if df["sma20"].iloc[-1] > df["sma50"].iloc[-1]:
        return "BUY"
    else:
        return "SELL"

# -----------------------------
# 📌 MAIN GOLD SIGNAL SENDER
# -----------------------------
def send_gold_signal():
    # Price
    entry = get_xauusd_price()

    # Fake 60-candle data for SMA calculation (replace with real source later)
    df = pd.DataFrame({"close": [entry] * 60})

    signal = generate_signal(df)

    # TP & SL calculation
    tp1 = entry + 0.20 if signal == "BUY" else entry - 0.20
    tp2 = entry + 0.40 if signal == "BUY" else entry - 0.40
    tp3 = entry + 0.60 if signal == "BUY" else entry - 0.60
    tp4 = entry + 0.80 if signal == "BUY" else entry - 0.80
    tp5 = entry + 1.00 if signal == "BUY" else entry - 1.00
    sl = entry - 0.40 if signal == "BUY" else entry + 0.40

    # Chart screenshot
    chart_path = get_chart("XAUUSD")

    # VIP style message
    msg = f"""
⚡ **GOLD XAUUSD SIGNAL** ⚡
Time: {datetime.now().strftime('%I:%M %p')}

**Signal:** {signal}
**Entry:** {entry}

🎯 **TARGETS**
TP1 → {tp1}
TP2 → {tp2}
TP3 → {tp3}
TP4 → {tp4}
TP5 → {tp5}

🛑 **Stop Loss:** {sl}
    """

    with open(chart_path, "rb") as img:
        bot.sendPhoto(chat_id=CHAT_ID, photo=img, caption=msg, parse_mode="Markdown")

    print("Gold Signal Sent!")

# Run once (GitHub Actions will trigger this file every minute)
if __name__ == "__main__":
    send_gold_signal()
