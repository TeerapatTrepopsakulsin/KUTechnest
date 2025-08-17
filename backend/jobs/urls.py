from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, PostViewSet


router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
