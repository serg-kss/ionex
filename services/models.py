from django.db import models
from tinymce.models import HTMLField


class OrderService(models.Model):
    name = models.CharField(max_length=150, verbose_name="ФИО клиента")
    email = models.EmailField(verbose_name="Контактный email")
    phone = models.CharField(verbose_name="Контактный номер телефона")
    service= models.CharField(verbose_name="Заказанная услуга")

    class Meta:
        db_table = "orderservices"
        verbose_name = "Заказанная услуга"
        verbose_name_plural = "Заказанные услуги"

    def __str__(self):
        return self.name


class CategoriesServices(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название раздела услуг")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )
    description = models.CharField(unique=False, blank=True, null=True, verbose_name="Краткое описание услуги")
    seo = models.CharField(max_length=160, unique=False, blank=True, null=True, verbose_name="сео")
    

    class Meta:
        db_table = "categoryservices"
        verbose_name = "Категория услуга"
        verbose_name_plural = "Категория услуги"

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название услуги")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )
    category = models.ForeignKey(
        to=CategoriesServices, on_delete=models.CASCADE, verbose_name="Раздел услуг"
    )
    content = HTMLField(unique=False, blank=True, null=True, verbose_name="Контент")
    seo = models.CharField(max_length=160, unique=False, blank=True, null=True, verbose_name="сео")

    class Meta:
        db_table = "service"
        verbose_name = "Услугу"
        verbose_name_plural = "услуги"
        ordering = ("id",)

    def __str__(self):
        return f'{self.name}'