
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from authapp.views import LoginView, LogoutView, RefreshView
from jobs.views import (
    StudentRegisterView, CompanyRegisterView, MeView, EmailTokenObtainPairView,
    PendingStudentsListView, ApproveStudentView,
    PendingCompaniesListView, ApproveCompanyView,
    CompanyViewSet, PostViewSet, StudentViewSet,
    StudentMeView, CompanyMeView,
)




router = DefaultRouter()
router.register(r"companies", CompanyViewSet, basename="company")
router.register(r"posts", PostViewSet, basename="post")
router.register(r"students", StudentViewSet, basename="student")

def google_auth_view():
    from authapp.views import GoogleAuthView  # imported only when URL is resolved
    return GoogleAuthView.as_view()


urlpatterns = [
    path("admin/", admin.site.urls),

    # ViewSets
    path("api/", include(router.urls)),

    # Auth & registration
    path("api/students/register/", StudentRegisterView.as_view()),
    path("api/companies/register/", CompanyRegisterView.as_view()),
    path("api/auth/login/", EmailTokenObtainPairView.as_view()),
    path("api/auth/me/", MeView.as_view()),

    # Admin approval endpoints
    path("api/admin/students/pending/", PendingStudentsListView.as_view()),
    path("api/admin/students/<int:user_id>/approve/",
         ApproveStudentView.as_view()),
    path("api/admin/companies/pending/", PendingCompaniesListView.as_view()),
    path("api/admin/companies/<int:user_id>/approve/",
         ApproveCompanyView.as_view()),

    # Student
    path("api/students/register/", StudentRegisterView.as_view(), name="students-register"),
    path("api/students/me/",       StudentMeView.as_view(),       name="students-me"),

    # Company (new)
    path("api/companies/register/", CompanyRegisterView.as_view(), name="companies-register"),
    path("api/companies/me/",       CompanyMeView.as_view(),       name="companies-me"),

    #Google Aouth
    path("auth/google/", google_auth_view(), name="auth_google"),

    ]

