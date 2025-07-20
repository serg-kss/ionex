from django import template
from main.models import Contacts


register = template.Library()
record = Contacts.objects.first()

@register.simple_tag()
def tag_contacts_email():
    email = record.email
    return email


@register.simple_tag()
def tag_contacts_phone():
    phone = record.phone
    return phone

@register.simple_tag()
def tag_contacts_address():
    address = record.address
    return address


@register.simple_tag()
def tag_contacts_instagram():
    instagram = record.instagram
    return instagram

@register.simple_tag()
def tag_contacts_facebook():
    facebook = record.facebook
    return facebook
