
from django.urls import include, path
from rest_framework.routers import DefaultRoute
from .views import CompanyViewSet, PostViewSet, StudentViewSet
from django.contrib import admin

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'posts', PostViewSet)
router.register(r'students', StudentViewSet)

urlpatterns = router.urls

