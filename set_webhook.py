# Запусти этот скрипт ОДИН РАЗ после деплоя на Vercel
# Он скажет Telegram куда слать сообщения

import urllib.request

TOKEN = "ВСТАВЬ_ТОКЕН_БОТА_СЮДА"
VERCEL_URL = "ВСТАВЬ_АДРЕС_VERCEL_СЮДА"  # например: https://my-bot.vercel.app

url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={VERCEL_URL}/api/webhook"

with urllib.request.urlopen(url) as response:
    print(response.read().decode())
