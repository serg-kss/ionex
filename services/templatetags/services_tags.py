from django import template
from services.models import CategoriesServices


register = template.Library()


@register.simple_tag()
def tag_categories_services():
    return CategoriesServices.objects.all()