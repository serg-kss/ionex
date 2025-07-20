from django.contrib import admin
from blog.models import CategoriesBlog, Articles


@admin.register(CategoriesBlog)
class CategoriesBlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name"]


@admin.register(Articles)
class ArticlesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "published_date","category", "author"]
