
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CompanyViewSet, PostViewSet, StudentRegisterView, StudentMeView,StudentViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Student endpoints
    path('students/register/', StudentRegisterView.as_view(), name='student-register'),
    path('students/me/', StudentMeView.as_view(), name='student-me'),

]
