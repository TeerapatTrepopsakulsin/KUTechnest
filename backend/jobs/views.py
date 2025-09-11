# jobs/views.py
from django.db.models import F, IntegerField
from django.db.models.functions import Cast, Replace
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Company, Post
from .serializers import CompanySerializer, PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("company").order_by("-id")
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description", "company__name", "location", "salary", "work_field"]
    ordering_fields = ["id", "created_at"]  # salary käsitellään customissa
    ordering = ["-id"]

    def get_permissions(self):

        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticatedOrReadOnly()]
        return [AllowAny()]

    def _with_salary_number(self, qs):
        """
        Luo annotaation salary_num poistamalla pilkut ja 'THB' ja castaa intiksi.
        Tukee muotoja esim: '60,000', 'THB 45,000', '45000'
        """
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
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        return Response(self.get_serializer(qs, many=True).data)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def onsite_jobs(self, request):
        qs = self.filter_queryset(self.get_queryset().filter(onsite=True))
        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        return Response(self.get_serializer(qs, many=True).data)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def by_salary_range(self, request):
        """
        GET /api/posts/by_salary_range/?min=30000&max=60000
        Palauttaa postaukset joiden salary_num on rajojen sisällä.
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

        # Salli hakusanat & järjestys myös tälle listalle
        qs = self.filter_queryset(qs)
        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        return Response(self.get_serializer(qs, many=True).data)


from django.db.models import Value



class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by("id")  # poistaa UnorderedObjectListWarningin
    serializer_class = CompanySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "location"]
    ordering_fields = ["id", "name"]
    ordering = ["id"]

    @action(detail=True, methods=["get"], permission_classes=[AllowAny])
    def posts(self, request, pk=None):
        """
        GET /api/companies/{id}/posts/
        Listaa yrityksen postaukset uusin ensin.
        """
        company = self.get_object()
        qs = Post.objects.filter(company=company).order_by("-created_at")
        # Paginate + serialisoi PostSerializerillä
        page = self.paginate_queryset(qs)
        if page is not None:
            data = PostSerializer(page, many=True, context=self.get_serializer_context()).data
            return self.get_paginated_response(data)
        data = PostSerializer(qs, many=True, context=self.get_serializer_context()).data
        return Response(data)
