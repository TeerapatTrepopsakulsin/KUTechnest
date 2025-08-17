from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company, Post
from .serializers import CompanySerializer, PostSerializer, PostCreateSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'location']

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        """Get all posts for a specific company"""
        company = self.get_object()
        posts = company.posts.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('company').all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company', 'onsite', 'location']
    search_fields = ['title', 'position', 'company__name', 'requirement', 'description']
    ordering_fields = ['created_at', 'salary', 'min_year']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer

    @action(detail=False, methods=['get'])
    def remote_jobs(self, request):
        """Get all remote jobs (onsite=False)"""
        remote_posts = self.queryset.filter(onsite=False)
        serializer = self.get_serializer(remote_posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def onsite_jobs(self, request):
        """Get all onsite jobs (onsite=True)"""
        onsite_posts = self.queryset.filter(onsite=True)
        serializer = self.get_serializer(onsite_posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_salary_range(self, request):
        """Filter jobs by salary range"""
        min_salary = request.query_params.get('min_salary', 0)
        max_salary = request.query_params.get('max_salary', None)

        queryset = self.queryset.filter(salary__gte=min_salary)
        if max_salary:
            queryset = queryset.filter(salary__lte=max_salary)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)