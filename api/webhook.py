import os
import json
import asyncio
from http.server import BaseHTTPRequestHandler
import urllib.request

TOKEN = "8759265616:AAHOPrxbFTpsvYOuPsyw-INbmQDv6GnaUmo"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = json.dumps({"chat_id": chat_id, "text": text}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        
        message = body.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")
        
        if chat_id:
            if text == "/start":
                send_message(chat_id, "Калькулятор потери напряжения ⚡\n\nФормула:\nU = 30 * I * L / S\n\nОтправь данные через пробел:\nI L S\n\nПример:\n50 0.8 16")
            else:
                try:
                    I, L, S = map(float, text.split())
                    U = 30 * I * L / S
                    send_message(chat_id, f"Результат:\nI = {I} A\nL = {L} км\nS = {S} мм²\n\nПотеря напряжения U = {U:.2f} В")
                except:
                    send_message(chat_id, "Ошибка ⚠️\nВведи 3 числа через пробел:\nI L S\n\nПример:\n50 0.8 16")
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")
