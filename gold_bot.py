import requests
import telegram
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("BOT_TOKEN and CHAT_ID environment variables are required")

bot = telegram.Bot(token=BOT_TOKEN)

def get_xauusd_price():
    url = "https://api.exchangerate.host/latest?base=XAU&symbols=USD"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        # Check if keys exist
        if "rates" not in data or "USD" not in data["rates"]:
            print("Unexpected API response format:", data)
            return None

        return float(data["rates"]["USD"])
    except requests.RequestException as e:
        print(f"Network/API request error: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing price: {e}")
        return None

def send_gold_signal():
    price = get_xauusd_price()
    if price is None:
        print("Price fetch failed, skipping signal.")
        return

    signal = "SELL" if int(price) % 2 == 0 else "BUY"

    if signal == "SELL":
        tp1 = price - 2
        tp2 = price - 4
        tp3 = price - 6
        tp4 = price - 8
        tp5 = price - 10
        sl  = price + 4
    else:
        tp1 = price + 2
        tp2 = price + 4
        tp3 = price + 6
        tp4 = price + 8
        tp5 = price + 10
        sl  = price - 4

    msg = f"""📉 **XAUUSD {signal} NOW**

💰 PRICE: {price}

🎯 TP1: {tp1}
🎯 TP2: {tp2}
🎯 TP3: {tp3}
🎯 TP4: {tp4}
🎯 TP5: {tp5}

❌ SL: {sl}
"""

    try:
        bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)
        print("Signal sent successfully.")
    except telegram.error.TelegramError as e:
        print(f"Telegram send_message error: {e}")

if __name__ == "__main__":
    send_gold_signal()
