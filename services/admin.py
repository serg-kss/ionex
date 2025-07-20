from django.contrib import admin
from services.models import CategoriesServices, Service, OrderService


@admin.register(CategoriesServices)
class CategoriesServicesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "category"]


@admin.register(OrderService)
class OrderServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "service"]    