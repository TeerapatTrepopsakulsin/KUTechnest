from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import IntegerField
from django.db.models.functions import Cast, Replace

from .models import Company, Post
from .serializers import CompanySerializer, PostSerializer, PostCreateSerializer


# -------------------------------
# Company ViewSet
# -------------------------------
class CompanyViewSet(viewsets.ModelViewSet):
    # Base queryset: fetch all companies
    queryset = Company.objects.all()

    # Serializer used for Company objects
    serializer_class = CompanySerializer

    # Anyone can read, but write operations require authentication
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable simple search by company name or location
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'location']

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def posts(self, request, pk=None):
        """
        Custom endpoint: GET /api/companies/<id>/posts/
        → Returns all posts for a specific company (paginated if needed)
        """
        company = self.get_object()
        # If your ForeignKey uses related_name='posts', you can use company.posts
        qs = company.posts.all().order_by('-created_at')

        # Apply pagination if enabled
        page = self.paginate_queryset(qs)
        if page is not None:
            ser = PostSerializer(page, many=True)
            return self.get_paginated_response(ser.data)

        ser = PostSerializer(qs, many=True)
        return Response(ser.data)


# -------------------------------
# Post ViewSet
# -------------------------------
class PostViewSet(viewsets.ModelViewSet):
    # Fetch all posts and join related company in one query for optimization
    queryset = Post.objects.select_related('company').all()

    # Default permission: read allowed for anyone, write requires authentication
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable filtering, search, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Fields that can be filtered directly via query params
    # Example: ?company=1&onsite=true
    filterset_fields = ['company', 'onsite', 'location']

    # Fields included in search (?search=keyword)
    search_fields = ['title', 'work_field', 'company__name', 'requirement', 'description']

    # Fields that can be ordered (?ordering=salary or ?ordering=-created_at)
    ordering_fields = ['created_at', 'salary', 'min_year']

    # Default ordering (most recent posts first)
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        Use a different serializer when creating a post (PostCreateSerializer),
        otherwise use the default PostSerializer for reading/updating.
        """
        return PostCreateSerializer if self.action == 'create' else PostSerializer

    # -------------------------------
    # Custom Endpoints
    # -------------------------------

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def remote_jobs(self, request):
        """
        GET /api/posts/remote_jobs/
        → Return all jobs where onsite=False (remote jobs)
        """
        qs = self.get_queryset().filter(onsite=False)
        page = self.paginate_queryset(qs)
        ser = PostSerializer(page or qs, many=True)
        return self.get_paginated_response(ser.data) if page is not None else Response(ser.data)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def onsite_jobs(self, request):
        """
        GET /api/posts/onsite_jobs/
        → Return all jobs where onsite=True (onsite jobs)
        """
        qs = self.get_queryset().filter(onsite=True)
        page = self.paginate_queryset(qs)
        ser = PostSerializer(page or qs, many=True)
        return self.get_paginated_response(ser.data) if page is not None else Response(ser.data)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def by_salary_range(self, request):
        """
        GET /api/posts/by_salary_range/?min_salary=10000&max_salary=30000
        → Filter jobs by salary range
        Works even if salary is stored as a string like "66,000"
        """
        def to_int(q, key, default=None):
            v = q.get(key, None)
            if v in (None, ''):
                return default
            try:
                return int(v)
            except ValueError:
                return None

        # Parse query params
        min_salary = to_int(request.query_params, 'min_salary', 0)
        max_salary = to_int(request.query_params, 'max_salary', None)

        # Validation
        if min_salary is None or (max_salary is None and 'max_salary' in request.query_params and request.query_params['max_salary'] != ''):
            return Response({"detail": "min_salary/max_salary must be integers"}, status=400)

        qs = self.get_queryset().annotate(
            salary_num=Cast(Replace('salary', ',', ''), IntegerField())
        )
        if min_salary is not None:
            qs = qs.filter(salary_num__gte=min_salary)
        if max_salary is not None:
            qs = qs.filter(salary_num__lte=max_salary)

        # Apply pagination if enabled
        page = self.paginate_queryset(qs)
        ser = PostSerializer(page or qs, many=True)
        return self.get_paginated_response(ser.data) if page is not None else Response(ser.data)
