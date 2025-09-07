"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from jobs.views import google_login_api, me_api, register_api
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("jobs.urls")),

    path("api/auth/register/", register_api, name="register"),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="jwt"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),

    # Google flow (ID token -> our JWT)
    path("api/auth/google/", google_login_api, name="google-login"),

    # Auth check
    path("api/me/", me_api, name="me"),
]

