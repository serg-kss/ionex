from django.contrib import admin
from goods.models import Categories, Products

# Register your models here.

# admin.site.register(Categories)
# admin.site.register(Products)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "ceo"]


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "quantity", "price", "discount"]
    list_editable= ["quantity", "price", "discount"]
    search_fields = ["name", "price"]
    list_filter =["quantity", "price", "discount", "category"]
    fields =[
        "name",
        "category",
        "slug",
        "description",
        "equipment",
        "characteristics",
        "image",
        ("price", "discount"),
        "quantity",
        "ceo",
    ]

from .models import CloudTest

admin.site.register(CloudTest)