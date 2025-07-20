from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render
from orders.models import Order, OrderItem
from carts.models import Cart
from orders.forms import CreateOrderForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import os
from .utils import send_order_confirmation, EmailMessage
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


API_KEY = os.getenv("NP_KEY")  # ключ храним в переменных окружения


@csrf_exempt
def np_proxy(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        body = request.body.decode("utf-8")
        data = json.loads(body)

        method = data.get("method")
        properties = data.get("properties", {})

        if not method:
            return JsonResponse({"error": "Method is required"}, status=400)

        payload = {
            "apiKey": API_KEY,
            "modelName": "Address",
            "calledMethod": method,
            "methodProperties": properties,
        }

        response = requests.post("https://api.novaposhta.ua/v2.0/json/", json=payload)

        return JsonResponse(response.json())

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


User = get_user_model()

@login_required
def create_order(request):
    if request.method == "POST":
        form = CreateOrderForm(data=request.POST)
        print("POST go on")
        if form.is_valid():
            print("valid form")
            try:
                print("valid form")
                with transaction.atomic():
                    user = request.user
                    cart_items = Cart.objects.filter(user=user)
                    user_db = User.objects.get(username=request.user.username)
                    customer_name = f'{form.cleaned_data["first_name"]} {form.cleaned_data["last_name"]}'
                    customer_email = form.cleaned_data["email"]
                    if cart_items.exists():
                        user_db.first_name = form.cleaned_data["first_name"]
                        user_db.last_name = form.cleaned_data["last_name"]
                        user_db.phone_number = form.cleaned_data["phone_number"]
                        user_db.email = form.cleaned_data["email"]
                        user_db.save()
                        # создать заказ
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data["phone_number"],
                            delivery_address=f'Область: {form.cleaned_data["region"]}. НП: {form.cleaned_data["city"]}. Відділення: {form.cleaned_data["warehouse"]}',
                            payment_on_get=form.cleaned_data["payment_on_get"],
                        )
                        
                        product_name = []
                        total_amount = 0
                        # создать заказанные товары
                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.name
                            price = cart_item.product.sell_price()
                            quantity = cart_item.quantity

                            # product_name += f'- {cart_item.product.name} цена за шт. {cart_item.product.sell_price()} UAH - {cart_item.quantity} шт\n'
                            product_name.append(
                                {
                                    "product_name": cart_item.product.name,
                                    "price_per_item": cart_item.product.sell_price(),
                                    "quantity": cart_item.quantity,
                                }
                            )
                            total_amount += (
                                cart_item.product.sell_price() * cart_item.quantity
                            )

                            if product.quantity < quantity:
                                raise ValidationError(
                                    f"Недостаточное количество товара {name} на складе в наличии {product.quantity}"
                                )

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )
                            product.quantity -= quantity
                            product.save()

                        # очистить корзину пользователя после создания заказа
                        cart_items.delete()
                        email_message = EmailMessage(
                            customer_name="".join(map(str, customer_name)),
                            product_name=product_name,
                            total_amount=total_amount,
                            customer_email=customer_email,
                            user=user_db,
                            delivery=f'НП: {form.cleaned_data["city"]}. Відділення: {form.cleaned_data["warehouse"]}',
                            payment=form.cleaned_data["payment_on_get"],
                        )
                        send_order_confirmation(email_message)
                        messages.success(request, "Замовлення оформлене. Дякуємо!")
                        return redirect("main:index")
            except ValidationError as e:
                print("huita")
                print(form.errors)
                messages.success(request, str(e))
                return redirect("cart:order")
        else:
            print("Форма не валидна")
            print(form.errors)
            print(request.POST)
    else:
        
        initial = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }

        form = CreateOrderForm(initial=initial)

    context = {"title": "Оформлення замовлення", "form": form, "order": True}
    return render(request, "orders/create_order.html", context=context)
