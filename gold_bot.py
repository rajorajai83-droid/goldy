import requests
import telegram
import os
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telegram.Bot(token=BOT_TOKEN)

def get_xauusd_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=XAUUSD"
    res = requests.get(url).json()
    return float(res["price"])

def send_gold_signal():
    price = get_xauusd_price()

    # Simple Auto Logic
    if price % 2 == 0:
        signal = "SELL"
    else:
        signal = "BUY"

    tp1 = price - 2 if signal == "SELL" else price + 2
    tp2 = price - 4 if signal == "SELL" else price + 4
    tp3 = price - 6 if signal == "SELL" else price + 6
    tp4 = price - 8 if signal == "SELL" else price + 8
    tp5 = price - 10 if signal == "SELL" else price + 10
    sl  = price + 4 if signal == "SELL" else price - 4

    msg = f"""
📉 **XAUUSD {signal} NOW**

💰 PRICE: {price}

🎯 TP1: {tp1}
🎯 TP2: {tp2}
🎯 TP3: {tp3}
🎯 TP4: {tp4}
🎯 TP5: {tp5}

❌ SL: {sl}
"""

    bot.send_message(chat_id=CHAT_ID, text=msg)

if __name__ == "__main__":
    send_gold_signal()
