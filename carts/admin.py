from django.contrib import admin

from carts.models import Cart

# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "product__name", "quantity", "created_timestamp"]
    list_filter = ["created_timestamp", "user", "product__name"]
