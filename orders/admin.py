from django.contrib import admin

from orders.models import Order, OrderItem

class OrderItemTabulareAdmin(admin.TabularInline):
    model = OrderItem
    fields = "product", "name", "price", "quantity"
    search_fields = (
        "product",
        "name",
    )
    extra = 0

class OrderTabulareAdmin(admin.TabularInline):
    model = Order
    fields = (
        "status",
        "payment_on_get",
        "is_paid",
        "created_timestamp",
    )
    search_fields = (
        "payment_on_get",
        "is_paid",
        "created_timestamp",
    )
    readonly_fields = ("created_timestamp",)
    extra = 0

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = "order", "product", "name", "price", "quantity"
    search_fields = (
        "order",
        "product",
        "name",
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display ="get_user_name", "id", "status", "payment_on_get", "is_paid", "created_timestamp"
    search_fields = (
        "id",
    )
    readonly_fields = ("created_timestamp",)
    list_filter = (
        "status",
        "payment_on_get",
        "is_paid",
        "created_timestamp", 
    )

    def get_user_name(self, object):
        return f'{object}'
    get_user_name.short_description = "Клиент"
   
        
    inlines = (OrderItemTabulareAdmin,)

