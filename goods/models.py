from django.db import models
from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )
    ceo = models.TextField(max_length=160, blank=True, null=True, verbose_name="ceo")

    class Meta:
        db_table = "category"
        verbose_name = "Категорию"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название")
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )
    description = HTMLField(unique=False, blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(
        upload_to="goods_images", blank=True, null=True, verbose_name="Изображение"
    )
    price = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2, verbose_name="Цена"
    )
    discount = models.DecimalField(
        default=0.00, max_digits=7, decimal_places=2, verbose_name="Скидка процент"
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    category = models.ForeignKey(
        to=Categories, on_delete=models.CASCADE, verbose_name="Категория Товара"
    )
    equipment = HTMLField(unique=False, blank=True, null=True, verbose_name="Комплектация")
    characteristics = HTMLField(unique=False, blank=True, null=True, verbose_name="Основные характеристики")
    ceo = models.TextField(max_length=160, blank=True, null=True, verbose_name="ceo")

    class Meta:
        db_table = "product"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ("id",)

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})
    
    
    def display_id(self):
        return f"{self.id:05}"
    
    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        
        return self.price


class CloudTest(models.Model):
    image = models.ImageField(upload_to="cloud_test/", blank=True, null=True, verbose_name="Изображение")
