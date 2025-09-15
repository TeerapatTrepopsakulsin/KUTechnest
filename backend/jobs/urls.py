from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, PostViewSet, StudentViewSet
from django.contrib import admin

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'posts', PostViewSet)
router.register(r'students', StudentViewSet)

urlpatterns = router.urls

