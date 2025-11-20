# chart.py
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_chart(symbol):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    url = f"https://www.tradingview.com/chart/?symbol=OANDA:{symbol}"
    driver.get(url)
    time.sleep(5)

    path = f"{symbol}.png"
    driver.save_screenshot(path)
    driver.quit()
    return path
