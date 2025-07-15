import os
from flask import Flask, request
import requests

app = Flask(__name__)

BITRIX24_WEBHOOK_URL = os.getenv("BITRIX24_WEBHOOK_URL")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def send_to_telegram(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, json=data)

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        message_text = data["message"].get("text", "")

        # Bitrix24 ga yuborish
        if message_text and BITRIX24_WEBHOOK_URL:
            requests.post(BITRIX24_WEBHOOK_URL, json={"fields": {"TITLE": message_text}})
            send_to_telegram(chat_id, "Xabaringiz Bitrix24 ga yuborildi.")
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
