from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from blog.models import Articles
from blog.models import CategoriesBlog
from django.core.paginator import Paginator


def blog_main(request):

    blog = CategoriesBlog.objects.all()
    articles = Articles.objects.all()

    array = []

    for topic in blog:
        index = 0
        for article in articles:
            if article.category == topic:
                index = index + 1
        array.append({"topic": topic, "index": index})

    paginator = Paginator(articles, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "title": "ІОНЕКС - Наш блог",
        "section_name": "Блог",
        "blog": array,
        "articles": articles,
        "page_obj": page_obj,
    }

    return render(request, "blog/blog_main.html", context=context)


def blog(request, blog_slug):

    blog = CategoriesBlog.objects.get(slug=blog_slug)
    seo = blog.seo
    articles = Articles.objects.filter(category=blog)

    paginator = Paginator(articles, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    blog_m = CategoriesBlog.objects.all()
    articles_m = Articles.objects.all()

    array = []

    for topic in blog_m:
        index = 0
        for article in articles_m:
            if article.category == topic:
                index = index + 1
        array.append({"topic": topic, "index": index})

    context = {
        "title": blog.name,
        "section_name": blog.name,
        "slug_url": blog_slug,
        "articles": articles,
        "blog": array,
        "page_obj": page_obj,
        "seo": seo,
    }

    return render(request, "blog/blog_main.html", context=context)


def article(request, article_slug):
    blog = CategoriesBlog.objects.all()
    articles = Articles.objects.all()

    array = []

    for topic in blog:
        index = 0
        for article in articles:
            if article.category == topic:
                index = index + 1
        array.append({"topic": topic, "index": index})

    article = Articles.objects.get(slug=article_slug)

    context = {"article": article, "blog": array, "title": article.name, "seo": article.seo,}
    return render(request, "blog/blog-details.html", context=context)


@csrf_exempt
def image_upload(request):
    if request.method == "POST":
        image = request.FILES.get("file")
        if not image:
            return JsonResponse({"error": "Нет изображения"}, status=400)

        filename = default_storage.save(
            f"uploads/{image.name}", ContentFile(image.read())
        )
        image_url = f"{settings.MEDIA_URL}{filename}"
        return JsonResponse({"location": image_url})

    return JsonResponse({"error": "Неверный метод"}, status=400)
