from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, render

from goods.utils import q_search
from goods.models import Products, Categories


def catalog(request, category_slug=None):

    
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)
    category = ''
    title = ''

    if category_slug == "vsi-tovary":
        goods = Products.objects.all()
        category = 'Всі товари'
        title = 'ІОНЕКС - Товари'
        seo = 'Купити ренгенозахисні товари, ІОНЕКС, ренген обладнання'

    elif query:
        goods = q_search(query)
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    if on_sale:
        goods = goods.filter(discount__gt=0)
    
    
    if order_by and order_by != "default":
        goods = goods.order_by(order_by)
        


    if category_slug != 'vsi-tovary':
       list = Categories.objects.filter(slug = category_slug)
       category = list[0].name
       title = list[0].name
       seo = list[0].ceo

    paginator = Paginator(goods, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    
    context = {
        "title": title, 
        "goods": goods, 
        "slug_url": category_slug,
        "category": category,
        "page_obj": page_obj,
        "seo": seo
    }
          
    return render(request, "goods/catalog.html", context)


def product(request, product_slug):

    product = Products.objects.get(slug=product_slug)

    context = {
        "product": product,
        "title": product.name,
        "seo": product.ceo
        }
    return render(request, "goods/product1.html", context=context)
