from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from google.oauth2 import id_token
from google.auth.transport import requests as g_requests
from rest_framework_simplejwt.tokens import RefreshToken
from jobs.models import Student, Company

User = get_user_model()


def _unique_username_from_email(email: str) -> str:
    base = (email.split("@")[0] or "user").lower()[:150]
    candidate = base
    i = 1
    while User.objects.filter(username=candidate).exists():
        i += 1
        candidate = (base + str(i))[:150]
    return candidate


def _resolve_role(user):
    if user.is_superuser or user.is_staff:
        return "admin"
    if hasattr(user, "company"):
        return "company"
    if hasattr(user, "student"):
        return "student"
    return "user"


class GoogleLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        idt = request.data.get("id_token")
        role = (request.data.get("role") or "student").strip().lower()
        if not idt:
            return Response({"ok": False, "error": "id_token missing"}, status=400)

        try:
            info = id_token.verify_oauth2_token(idt, g_requests.Request(), audience=None)
        except Exception as e:
            return Response({"ok": False, "error": f"invalid token: {e}"}, status=400)

        aud = info.get("aud")
        allowed = getattr(settings, "GOOGLE_CLIENT_IDS", [])
        if aud not in allowed:
            return Response({"ok": False, "error": "audience mismatch"}, status=400)

        email = info.get("email")
        if not email or not info.get("email_verified", False):
            return Response({"ok": False, "error": "email not verified"}, status=400)

        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": _unique_username_from_email(email)},
        )

        name = (info.get("name") or "").strip()
        if name and (not user.first_name and not user.last_name):
            parts = name.split(" ", 1)
            user.first_name = parts[0]
            if len(parts) > 1:
                user.last_name = parts[1]
            user.save()

        if role == "student" and not hasattr(user, "student"):
            Student.objects.create(user=user, name=name or None)
        elif role == "company" and not hasattr(user, "company"):
            Company.objects.create(user=user, name=name or "Company")

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response({
            "ok": True,
            "created": created,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": _resolve_role(user),
            },
            "access": access,
            "refresh": str(refresh),
            "google": {
                "sub": info.get("sub"),
                "aud": aud,
                "picture": info.get("picture"),
            }
        }, status=200)


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        u = request.user
        return Response({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "role": _resolve_role(u),
        })

