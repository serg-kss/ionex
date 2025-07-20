from django.urls import path
from blog import views


app_name = 'blog'


urlpatterns = [
    path("", views.blog_main, name="index_main"),
    path("<slug:blog_slug>/", views.blog, name="index"),
    path("article/<slug:article_slug>/", views.article, name="article"),
]