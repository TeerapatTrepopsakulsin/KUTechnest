from django.db.models import F, IntegerField, Value
from django.db.models.functions import Cast, Replace
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Company, Post
from .serializers import (
    CompanySerializer,
    PostListSerializer,
    PostDetailSerializer,
    PostCreateSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("company").order_by("-id")
    permission_classes = [AllowAny]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "title", "description", "long_description",
        "company__name", "location", "salary", "work_field"
    ]
    ordering_fields = ["id", "created_at"]  # salary handled via annotation
    ordering = ["-id"]

    filterset_fields = ["employment_type"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticatedOrReadOnly()]
        return [AllowAny()]

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
    queryset = Company.objects.all().order_by("id")
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
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
