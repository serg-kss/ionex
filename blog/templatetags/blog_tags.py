from django import template
from blog.models import CategoriesBlog


register = template.Library()


@register.simple_tag()
def tag_categories_blog():
    return CategoriesBlog.objects.all()