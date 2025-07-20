from django.contrib import admin
from .models import Contacts, Contact
from django.utils.timezone import localtime

# Register your models here.
admin.site.site_header = ' '
admin.site.site_title = 'Админ IOHEKC'

admin.site.register(Contacts)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "date"]

    def formatted_date(self, obj):
        return localtime(obj.date).strftime('%d.%m.%Y %H:%M')
    formatted_date.short_description = 'Дата отправки'