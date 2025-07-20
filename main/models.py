from django.db import models


class Contacts(models.Model):
    phone = models.CharField(verbose_name="Контактный номер телефона")
    email = models.EmailField(verbose_name="Контактный email")
    address = models.CharField(verbose_name="Адрес офиса")
    instagram = models.CharField(blank=True, null=True, verbose_name="Instagram")
    facebook = models.CharField(blank=True, null=True, verbose_name="Facebook")
    seo = models.CharField(max_length=160, unique=False, blank=True, null=True, verbose_name="сео стр главная и контакты")
    

    class Meta:
        db_table = "contact"
        verbose_name = "Контакт для сайта"
        verbose_name_plural = "Контакты для сайта"

    def __str__(self):
        return "Контактные данные IOHEKC"
    
class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    email = models.EmailField(verbose_name="Контактный email")
    message = models.TextField(verbose_name="Сообщение")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    class Meta:
        db_table = "message"
        verbose_name = "Сообщение клиента"
        verbose_name_plural = "Сообщения от клиентов"

    def __str__(self):
        return f"Вопрос {self.name}"