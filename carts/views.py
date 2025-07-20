from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login
from django.urls import reverse
from users.models import User
from carts.utils import get_user_carts
from carts.models import Cart
from goods.models import Products
from django.contrib.auth.models import AnonymousUser

import random
import string


def cart_add(request):

    product_id = request.POST.get("product_id")

    product = Products.objects.get(id=product_id)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)
    else:
        carts = Cart.objects.filter(
            session_key=request.session.session_key, product=product
        )
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            uname = "user_" + "".join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(6)
            )
            upass = "".join(
                random.choice(string.ascii_letters + string.digits + "!@#$%^&*()_")
                for _ in range(10)
            )
            new_user = User.objects.create_user(username=uname, password=upass)
            authenticate(new_user)

            if new_user is not None:
                login(request, new_user)
                Cart.objects.create(
                    session_key=request.session.session_key,
                    product=product,
                    quantity=1,
                    user=new_user,
                )

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/updated_cart.html", {"carts": user_cart}, request=request
    )

    response_data = {
        "message": "Товар в кошику!",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)


def cart_change(request):
    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")
    cart = Cart.objects.get(id=cart_id)
    cart.quantity = quantity
    cart.save()
    updated_quantity = cart.quantity
    cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"carts": cart}, request=request
    )
    response_data = {
        "message": "Кількість змінена",
        "cart_items_html": cart_items_html,
        "quaantity": updated_quantity,
    }

    return JsonResponse(response_data)


def cart_remove(request):

    cart_id = request.POST.get("cart_id")
    cart = Cart.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/updated_cart.html", {"carts": user_cart}, request=request
    )

    cart_items_html_1 = render_to_string(
        "carts/includes/included_cart.html", {"carts": user_cart}, request=request
    )

    response_data = {
        "message": "Видалено",
        "cart_items_html": cart_items_html,
        "cart_items_html_1": cart_items_html_1,
        "quantity_deleted": quantity,
    }

    return JsonResponse(response_data)
