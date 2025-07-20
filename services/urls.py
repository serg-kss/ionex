from django.urls import path
from services import views


app_name = 'services'


urlpatterns = [
    path("", views.all_services, name="all"),
    path("<slug:services_slug>/", views.services, name="index"),
    path("obrana-posluga/<slug:service_slug>/", views.service, name="service"),
]