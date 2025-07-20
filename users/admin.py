from django.contrib import admin
from django.utils.safestring import mark_safe

from orders.admin import OrderTabulareAdmin
from users.models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "is_superuser", "is_staff", "get_html_photo"]
    search_fields = ["name", "email"]

    inlines = [OrderTabulareAdmin]
    

    def get_html_photo(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50>")
        
    get_html_photo.short_description = "АВА"
