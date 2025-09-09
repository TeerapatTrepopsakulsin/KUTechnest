# jobs/views.py

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F, IntegerField, Value
from django.db.models.functions import Cast, Replace
from django.conf import settings

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from django_filters.rest_framework import DjangoFilterBackend

from google.oauth2 import id_token
from google.auth.transport import requests as grequests

from .models import Company, Post
from .serializers import (
    CompanySerializer,
    PostListSerializer,
    PostDetailSerializer,
    PostCreateSerializer,
)

User = get_user_model()


# ---------------------------
# Helpers
# ---------------------------

def _mint_tokens(user):
    """Create access/refresh JWT for a user."""
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}

def _clean_email(s: str) -> str:
    return (s or "").strip().lower()


# ---------------------------
# Public API: Auth endpoints
# ---------------------------

@api_view(["POST"])
@permission_classes([AllowAny])
def register_api(request):
    """
    Email/password registration (no external serializer needed).
    Body: { "email": "...", "password": "...", "first_name"?, "last_name"? }
    Username is set to email so you can log in with username=email at /api/auth/token/.
    """
    email = _clean_email(request.data.get("email"))
    password = request.data.get("password") or ""
    first_name = (request.data.get("first_name") or "").strip()
    last_name = (request.data.get("last_name") or "").strip()

    if not email:
        return Response({"email": ["This field is required."]}, status=400)
    if not password or len(password) < 8:
        return Response({"password": ["Password must be at least 8 characters."]}, status=400)
    if User.objects.filter(email__iexact=email).exists():
        return Response({"email": ["A user with this email already exists."]}, status=400)

    with transaction.atomic():
        user = User(username=email, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

    tokens = _mint_tokens(user)
    return Response(
        {
            "ok": True,
            "message": "Registered successfully.",
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            **tokens,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def google_login_api(request):
    """
    Google sign-in (ID token -> our JWT).
    Body: { "credential": "<Google ID token>" }
    """
    token = request.data.get("credential")
    if not token:
        return Response({"detail": "Missing credential"}, status=400)

    try:
        info = id_token.verify_oauth2_token(
            token,
            grequests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )
    except Exception:
        return Response({"detail": "Invalid Google token"}, status=400)

    if not info.get("email_verified"):
        return Response({"detail": "Email not verified"}, status=400)

    email = _clean_email(info.get("email"))
    full_name = (info.get("name") or email.split("@")[0]).strip()
    first_name, last_name = full_name, ""
    if " " in full_name:
        parts = full_name.split()
        first_name = parts[0]
        last_name = " ".join(parts[1:])

    user, created = User.objects.get_or_create(
        email=email,
        defaults={"username": email, "first_name": first_name, "last_name": last_name},
    )

    tokens = _mint_tokens(user)
    return Response(
        {
            "ok": True,
            "created": created,
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            **tokens,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_api(request):
    """Return the authenticated user's profile."""
    u = request.user
    return Response(
        {
            "id": u.id,
            "email": u.email,
            "username": u.get_username(),
            "first_name": u.first_name,
            "last_name": u.last_name,
        }
    )


# ---------------------------
# Resources: Posts & Companies
# ---------------------------

class PostViewSet(viewsets.ModelViewSet):
    """
    - Public reads (GET)
    - Auth required for writes (POST/PATCH/PUT/DELETE)
    - Search, ordering, filter by employment_type
    """
    queryset = Post.objects.select_related("company").order_by("-id")
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication, SessionAuthentication]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = [
        "title", "description", "long_description",
        "company__name", "location", "salary", "work_field"
    ]
    ordering_fields = ["id", "created_at"]  # salary handled via annotation
    ordering = ["-id"]
    filterset_fields = ["employment_type"]

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        if self.action == "retrieve":
            return PostDetailSerializer
        if self.action in ["create", "update", "partial_update"]:
            return PostCreateSerializer
        return PostDetailSerializer

    def _with_salary_number(self, qs):
        cleaned = Replace(
            Replace(
                Replace(F("salary"), Value("THB"), Value("")),
                Value(","), Value("")
            ),
            Value(" "), Value("")
        )
        return qs.annotate(salary_num=Cast(cleaned, IntegerField()))

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def remote_jobs(self, request):
        qs = self.filter_queryset(self.get_queryset().filter(onsite=False))
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(qs, many=True).data)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def onsite_jobs(self, request):
        qs = self.filter_queryset(self.get_queryset().filter(onsite=True))
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(qs, many=True).data)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def by_salary_range(self, request):
        """
        GET /api/posts/by_salary_range/?min=30000&max=60000
        """
        try:
            min_s = int(request.query_params.get("min", 0))
        except ValueError:
            min_s = 0
        try:
            max_s = int(request.query_params.get("max", 10**9))
        except ValueError:
            max_s = 10**9

        qs = self._with_salary_number(self.get_queryset()).filter(
            salary_num__gte=min_s, salary_num__lte=max_s
        )
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(self.get_serializer(page, many=True).data)
        return Response(self.get_serializer(qs, many=True).data)


class CompanyViewSet(viewsets.ModelViewSet):
    """
    - Public reads (GET)
    - Auth required for writes (POST/PATCH/PUT/DELETE)
    """
    queryset = Company.objects.all().order_by("id")
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication, SessionAuthentication]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ["name", "location"]
    ordering_fields = ["id", "name"]
    ordering = ["id"]

    @action(detail=True, methods=["get"], permission_classes=[AllowAny])
    def posts(self, request, pk=None):
        qs = Post.objects.filter(company=self.get_object()).order_by("-created_at")
        page = self.paginate_queryset(qs)
        if page is not None:
            data = PostDetailSerializer(page, many=True, context=self.get_serializer_context()).data
            return self.get_paginated_response(data)
        data = PostDetailSerializer(qs, many=True, context=self.get_serializer_context()).data
        return Response(data)
