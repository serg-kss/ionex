from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

import requests
import os

from orders.models import Order


class EmailMessage:
    def __init__(self, customer_name, total_amount, customer_email, product_name, user, delivery, payment):
        self.customer_name = customer_name
        self.product_name = product_name
        self.total_amount = total_amount
        self.customer_email = customer_email
        self.user = user
        self.delivery = delivery
        self.payment = payment


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
CHAT_ID = os.getenv("CHAT_ID")


def send_order_confirmation(order):
    order_db = (
        Order.objects.filter(user=order.user).order_by("created_timestamp").last()
    )
    order_id = order_db.pk
    order_phone_number = order_db.phone_number
    html_context = render_to_string(
        "custom_email.html",
        context={
            "order_id": order_id,
            "customer_name": order.customer_name,
            "product_name": order.product_name,
            "total_amount": order.total_amount,
            "payment": order.payment,
            "delivery": order.delivery,
        },
    )
    image_path = "static/deps/images/logo-mail.jpeg"
    email = EmailMultiAlternatives(
        subject="Підтвердження заказу ІОНЕКС",
        body="",
        from_email=settings.EMAIL_HOST_USER,
        to=[order.customer_email],
    )

    email.attach_alternative(html_context, "text/html")

    with open(image_path, "rb") as image_file:
        img = MIMEImage(image_file.read())
        img.add_header("Content-ID", "<image_id>")
        img.add_header("Content-Disposition", "inline", filename="image/jpeg")
        email.attach(img)

    email.send()

    """
    Отправка сообщения с заказом в Telegram.

    :param chat_id: ID чата клиента (в формате числа, например: 123456789)
    :param order_details: Детали заказа (строка)
    :return: Ответ от Telegram API (JSON)
    """

    product = ''
    for index, item in enumerate(order.product_name, start=1):
        product = product + f"Товар {index}: {item['product_name']}; ціна за шт: {item['price_per_item']}; Кількість: {item['quantity']};\n"

    try:
        payload = {
            "chat_id": CHAT_ID,
            "text": f"Новий Заказ на сайті! деталі заказу:\n\nЗаказ №{order_id}\nПокупець: {order.customer_name}\n{product}\nВсього {order.total_amount} грн.\nТелефон: {order_phone_number}\nДоставка: {order.delivery} \nОплата: {order.payment}\n\nГарного Вам дня! ☺",
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
