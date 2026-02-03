import asyncio
import os
import requests
from telegram import Bot

TOKEN = os.getenv("TOKEN")
ID_CHAT = int(os.getenv("ID_CHAT"))

bot = Bot(token=TOKEN)


def buscar_chollos():
    url = "https://www.vinted.es/api/v2/catalog/items"

    params = {
        "search_text": "nike",
        "page": 1,
        "per_page": 5
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    r = requests.get(url, headers=headers, params=params)
    data = r.json()

    chollos = []

    for item in data.get("items", []):
        titulo = item["title"]
        precio = item["price"]
        link = "https://www.vinted.es" + item["url"]

        chollos.append((titulo, precio, link))

    return chollos


async def main():
    while True:
        chollos = buscar_chollos()

        for titulo, precio, link in chollos:
            mensaje = f"🔥 CHOLLO\n{titulo}\n💰 {precio}€\n{link}"
            await bot.send_message(chat_id=ID_CHAT, text=mensaje)
            await asyncio.sleep(2)

        await asyncio.sleep(300)


asyncio.run(main())
