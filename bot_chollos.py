import asyncio
import time
import os
from telegram import Bot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

TOKEN = os.getenv("TOKEN")
ID_CHAT = int(os.getenv("ID_CHAT"))

bot = Bot(token=TOKEN)

def buscar_chollos():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://www.vinted.es/catalog?search_text=nike")
    time.sleep(6)

    # aceptar cookies
    try:
        botones = driver.find_elements(By.XPATH, "//button")
        for b in botones:
            if "acept" in b.text.lower():
                driver.execute_script("arguments[0].click();", b)
                time.sleep(2)
                break
    except:
        pass

    chollos = []
    items = driver.find_elements(By.CSS_SELECTOR, "a[href*='/items/']")

    for item in items[:5]:
        link = item.get_attribute("href")
        titulo = item.text.strip()
        chollos.append((titulo if titulo else "Producto Nike", link))

    driver.quit()
    return chollos

async def main():
    while True:
        chollos = buscar_chollos()

        for titulo, link in chollos:
            mensaje = f"🔥 CHOLLO\n{titulo}\n{link}"
            await bot.send_message(chat_id=CHAT_ID, text=mensaje)
            await asyncio.sleep(2)

        await asyncio.sleep(300)

asyncio.run(main())
