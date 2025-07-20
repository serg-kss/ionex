from django.urls import path
from .views import np_proxy
from orders import views

app_name = 'orders'

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
    path('api/novaposhta/', views.np_proxy, name='np_proxy'),
]
