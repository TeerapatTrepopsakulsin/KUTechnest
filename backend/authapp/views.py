from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView


# Google verification libs
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
#from authapp.views import GoogleAuthView

from .serializers import LoginSerializer

User = get_user_model()

def get_user_role_and_profile(user):
    """
    Return ('student'|'company'|'user', profile_dict).
    Adjust attribute access to your actual profile models.
    """
    role = "user"
    profile = {}

    # Example: OneToOne relations with related_name 'student' and 'company'
    if hasattr(user, "student"):
        role = "student"
        profile = {"full_name": getattr(user.student, "full_name", "")}
    elif hasattr(user, "company"):
        role = "company"
        profile = {"company_name": getattr(user.company, "name", "")}

    return role, profile


class LoginView(APIView):
    """
    Email + password login that returns JWTs and basic user info.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        role, profile = get_user_role_and_profile(user)

        return Response({
            "ok": True,
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": getattr(user, "first_name", "") or "",
                "last_name": getattr(user, "last_name", "") or "",
                "role": role,
                "profile": profile,
            },
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    Blacklist all refresh tokens for this user (logs out from all devices).
    Requires a valid ACCESS token in Authorization header.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken

        for token in OutstandingToken.objects.filter(user=request.user):
            BlacklistedToken.objects.get_or_create(token=token)

        return Response({"ok": True, "message": "Logged out successfully."})


class RefreshView(TokenRefreshView):
    """
    Standard SimpleJWT refresh. POST { "refresh": "<refresh_token>" }
    """
    permission_classes = [permissions.AllowAny]


class GoogleAuthView(APIView):
    """
    Accept a Google ID token (from Google Identity Services).
    Verifies it, creates/fetches a local user, and returns JWTs + role/profile.
    Accepts 'credential' (GIS default) or 'id_token' in the request body.
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # allow anonymous calls

    def post(self, request):
        raw_token = request.data.get("credential") or request.data.get("id_token")
        if not raw_token:
            return Response({"ok": False, "error": "Missing Google ID token."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            claims = google_id_token.verify_oauth2_token(raw_token, google_requests.Request())

            # Recommended audience check against your configured Client IDs
            allowed = getattr(settings, "GOOGLE_OAUTH_CLIENT_IDS", []) or []
            aud = claims.get("aud")
            if allowed and aud not in allowed:
                return Response({"ok": False, "error": "Invalid audience."}, status=400)

            # Basic issuer check
            if claims.get("iss") not in ("https://accounts.google.com", "accounts.google.com"):
                return Response({"ok": False, "error": "Invalid token issuer."}, status=400)

            email = claims.get("email")
            if not email:
                return Response({"ok": False, "error": "Email missing in Google token."}, status=400)

            if not claims.get("email_verified", False):
                return Response({"ok": False, "error": "Email not verified by Google."}, status=400)

            given_name = claims.get("given_name") or ""
            family_name = claims.get("family_name") or ""
            picture = claims.get("picture", "") or ""

            # Create or fetch the local user. Email is the unique identifier.
            user, created = User.objects.get_or_create(
                email=email,
                defaults={"first_name": given_name, "last_name": family_name},
            )

            # Ensure an unusable password for new Google users
            if created and hasattr(user, "set_unusable_password"):
                user.set_unusable_password()
                user.save(update_fields=["password"])

            # Optionally fill empty names from Google
            updated = False
            if not getattr(user, "first_name", "") and given_name:
                user.first_name = given_name; updated = True
            if not getattr(user, "last_name", "") and family_name:
                user.last_name = family_name; updated = True
            if updated:
                user.save()

            refresh = RefreshToken.for_user(user)
            role, profile = get_user_role_and_profile(user)

            return Response({
                "ok": True,
                "created": created,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name or "",
                    "last_name": user.last_name or "",
                    "role": role,
                    "profile": profile,
                    "avatar_url": picture,
                },
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=200)

        except ValueError as e:
            return Response({"ok": False, "error": f"Invalid Google token: {e}"}, status=400)
        except Exception as e:
            return Response({"ok": False, "error": f"Unexpected error: {e}"}, status=500)

