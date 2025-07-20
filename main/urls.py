
from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path("", views.index, name="index"),
    path("contacts/", views.contacts, name="about"),
]