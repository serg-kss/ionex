"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.urls import re_path

from app.settings import DEBUG

from blog.views import image_upload


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls", namespace="main")),
    path("catalog/", include("goods.urls", namespace="catalog")),
    path("blog/", include("blog.urls", namespace="blog")),
    path("poslugi/", include("services.urls", namespace="services")),
    path("user/", include("users.urls", namespace="user")),
    path("cart/", include("carts.urls", namespace="cart")),
    path("orders/", include("orders.urls", namespace="orders")),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path('tinymce/', include('tinymce.urls')),
    path('upload_image/', image_upload, name='tinymce_image_upload'),
]
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]


if DEBUG:
    urlpatterns = (
        [
            path("admin/", admin.site.urls),
            path("", include("main.urls", namespace="main")),
            path("catalog/", include("goods.urls", namespace="catalog")),
            path("blog/", include("blog.urls", namespace="blog")),
            path("poslugi/", include("services.urls", namespace="services")),
            path("user/", include("users.urls", namespace="user")),
            path("cart/", include("carts.urls", namespace="cart")),
            path("orders/", include("orders.urls", namespace="orders")),
            path(
                "password_reset/",
                auth_views.PasswordResetView.as_view(
                    template_name="registration/password_reset_form.html"
                ),
                name="password_reset",
            ),
            path(
                "password_reset_done/",
                auth_views.PasswordResetDoneView.as_view(
                    template_name="registration/password_reset_done.html"
                ),
                name="password_reset_done",
            ),
            path(
                "reset/<uidb64>/<token>/",
                auth_views.PasswordResetConfirmView.as_view(
                    template_name="registration/password_reset_confirm.html"
                ),
                name="password_reset_confirm",
            ),
            path(
                "reset_done/",
                auth_views.PasswordResetCompleteView.as_view(
                    template_name="registration/password_reset_complete.html"
                ),
                name="password_reset_complete",
            ),
            path('tinymce/', include('tinymce.urls')),
            
            path('upload_image/', image_upload, name='tinymce_image_upload'),

        ]
        + debug_toolbar_urls()
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
