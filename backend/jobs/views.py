from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company, Post
from .serializers import CompanySerializer, PostSerializer, PostCreateSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # ← GET vapaa, muut vaatii auth
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'location']

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def posts(self, request, pk=None):
        """Get all posts for a specific company (paginated)"""
        company = self.get_object()
        qs = company.posts.all().order_by('-created_at')
        page = self.paginate_queryset(qs)
        if page is not None:
            ser = PostSerializer(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = PostSerializer(qs, many=True)
        return Response(ser.data)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('company').all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # ← GET vapaa, muut auth
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company', 'onsite', 'location']
    search_fields = ['title', 'position', 'company__name', 'requirement', 'description']
    ordering_fields = ['created_at', 'salary', 'min_year']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def remote_jobs(self, request):
        """Get all remote jobs (onsite=False)"""
        qs = self.get_queryset().filter(onsite=False)
        page = self.paginate_queryset(qs)
        ser = self.get_serializer(page or qs, many=True)
        return self.get_paginated_response(ser.data) if page is not None else Response(ser.data)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def onsite_jobs(self, request):
        """Get all onsite jobs (onsite=True)"""
        qs = self.get_queryset().filter(onsite=True)
        page = self.paginate_queryset(qs)
        ser = self.get_serializer(page or qs, many=True)
        return self.get_paginated_response(ser.data) if page is not None else Response(ser.data)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def by_salary_range(self, request):
        """Filter jobs by salary range ?min_salary=10000&max_salary=30000"""
        def to_int(q, key, default=None):
            v = q.get(key, None)
            if v is None or v == '':
                return default
            try:
                return int(v)
            except ValueError:
                return None

        min_salary = to_int(request.query_params, 'min_salary', 0)
        max_salary = to_int(request.query_params, 'max_salary', None)
        if min_salary is None or (max_salary is None and 'max_salary' in request.query_params and request.query_params['max_salary'] != ''):
            return Response({"detail": "min_salary/max_salary must be integers"}, status=400)

        qs = self.get_queryset()
        if min_salary is not None:
            qs = qs.filter(salary__gte=min_salary)
        if max_salary is not None:
            qs = qs.filter(salary__lte=max_salary)

        page = self.paginate_queryset(qs)
        ser = self.get_serializer(page or qs, many=True)
        return self.get_paginated_response(ser.data) if page is not None else Response(ser.data)
