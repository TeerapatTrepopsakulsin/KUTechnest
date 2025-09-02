
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, PostViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"companies", CompanyViewSet, basename="company")

urlpatterns = [
    path("", include(router.urls)),
]
