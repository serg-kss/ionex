from django import template
from main.models import Contacts


register = template.Library()
#record = Contacts.objects.first()

@register.simple_tag()
def tag_contacts_email():
    return 'ionex.xray@gmail.com'


@register.simple_tag()
def tag_contacts_phone():
    return '0978950558, 0935620518'

@register.simple_tag()
def tag_contacts_address():
    return 'м. Дніпро'


@register.simple_tag()
def tag_contacts_instagram():
    return 'https://www.instagram.com/ionex.ua?igsh=MTdleG9xMGRqdDY1Zg=='

@register.simple_tag()
def tag_contacts_facebook():
    return 'https://www.facebook.com/share/1KbWdAuJAm/'
