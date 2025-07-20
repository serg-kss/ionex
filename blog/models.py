from django.db import models
from tinymce.models import HTMLField


class CategoriesBlog(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Тематика статей")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )
    seo = models.CharField(max_length=160, unique=False, blank=True, null=True, verbose_name="сео")

    class Meta:
        db_table = "categoryblog"
        verbose_name = "Тема"
        verbose_name_plural = "Темы"

    def __str__(self):
        return self.name


class Articles(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название статьи")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Краткое описание статьи")
    category = models.ForeignKey(
        to=CategoriesBlog, on_delete=models.CASCADE, verbose_name="Тематика статей"
    )
    author = models.CharField(max_length=150, unique=False, verbose_name="Авторы")
    content = HTMLField(unique=False, blank=True, null=True, verbose_name="Контент")
    seo = models.CharField(max_length=160, unique=False, blank=True, null=True, verbose_name="сео")
    published_date = models.DateField(blank=True, null=True, verbose_name="Дата публикации")

    class Meta:
        db_table = "article"
        verbose_name = "Статью"
        verbose_name_plural = "Статьи"
        ordering = ("id",)

    def __str__(self):
        return f'{self.name}'