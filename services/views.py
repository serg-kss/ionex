from django.shortcuts import redirect, render
from services.models import Service
from services.models import CategoriesServices, OrderService
from django.contrib import messages
import re
from .utils import send_services_order_telegram


def all_services(request):

    list_of_services = CategoriesServices.objects.all()

    context = {
        "title": "ІОНЕКС - Наші послуги",
        "list_of_services": list_of_services,
        "seo": "послуги для ренгенкабінетів компанія ІОНЕКС"
    }

    return render(request, "services/services.html", context=context)


def services(request, services_slug):

    services = CategoriesServices.objects.get(slug=services_slug)
    list_of_services = Service.objects.filter(category=services)
    context = {
        "title": services.name,
        "seo": services.seo,
        "slug_url": services_slug,
        "list_of_services": list_of_services,
    }

    return render(request, "services/services.html", context=context)


def service(request, service_slug):
    service = Service.objects.get(slug=service_slug)

    context = {
        "service": service,
        "title": service.name,
        "seo": service.seo,
    }
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone", "").strip()

        if name and email and phone:
            if not re.fullmatch(r"\d{10}", phone):
                return render(
                    request,
                    "services/service-details.html",
                    {
                        "error": "Будь ласка напишіть в форматі: 0991111111 (10 цифр без пробідлв)",
                    },
                )
            OrderService.objects.create(
                name=name, email=email, phone=phone, service=service.name
            )
            send_services_order_telegram(
                {
                    "name": name,
                    "phone": phone,
                    "service": service.name
                }
            )
            messages.success(request, "Заявка відправлена")
            return redirect("/")
        else:
            error = "Не всі поля заповнено!"
            return render(request, "services/service-details.html", {"error": error})
    return render(request, "services/service-details.html", context=context)
