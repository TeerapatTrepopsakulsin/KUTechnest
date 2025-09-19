from django.urls import path
from .views import GoogleLoginView, MeView

urlpatterns = [
    path("google/", GoogleLoginView.as_view(), name="google_login"),
    path("me/", MeView.as_view(), name="whoami"),
]
