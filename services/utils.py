import requests
import os


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
CHAT_ID = os.getenv("CHAT_ID")

def send_services_order_telegram(order):


    try:
        payload = {
            "chat_id": CHAT_ID,
            "text": f"Новий Заказ послуги на сайті!\n\nЗамовник: {order['name']}\nТелефон: {order['phone']}\nПослуга: {order['service']}\n\nГарного Вам дня! ☺",
            "parse_mode": "HTML",  # Чтобы поддерживать форматирование HTML в сообщении
        }
        response = requests.post(TELEGRAM_API_URL, json=payload)
        response_data = response.json()

        if response.status_code != 200 or not response_data.get("ok"):
            raise Exception(f"Ошибка отправки сообщения: {response_data}")

        return response_data
    except Exception as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")
        raise