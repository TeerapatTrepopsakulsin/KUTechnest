from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, PostViewSet
from django.contrib import admin

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = router.urls

