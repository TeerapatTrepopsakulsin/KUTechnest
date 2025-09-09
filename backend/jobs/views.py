# jobs/views.py
from rest_framework import viewsets, filters, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company, Post, Student
from rest_framework_simplejwt.views import TokenViewBase

from rest_framework.permissions import IsAdminUser
from .serializers import (
    CompanySerializer,
    PostSerializer,
    PostCreateSerializer,
    StudentRegisterSerializer,
    StudentSerializer,
    CompanyRegisterSerializer,
    UserPublicSerializer,
    EmailTokenObtainPairSerializer,
)


class CompanyRegisterView(generics.CreateAPIView):
    """
    POST /api/companies/register/
    Body (JSON):
      {
        "name": "TechNest Co., Ltd.",        # required
        "website": "https://example.com",    # optional
        "location": "Bangkok",               # optional
        "description": "We build stuff.",    # optional
        "contacts": "hr@example.com"         # optional
      }

    Requirements:
    - Authorization: Bearer <access> (from /api/auth/google/)
    - The company is linked to request.user (OneToOne).
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CompanyRegisterSerializer
    queryset = Company.objects.all()


class CompanyMeView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/companies/me/       -> return current user's company profile
    PATCH  /api/companies/me/       -> partial update (name, website, location, etc.)
    DELETE /api/companies/me/       -> delete current user's company profile
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CompanySerializer  # reuse read serializer for responses

    def get_object(self):
        try:
            return Company.objects.get(user=self.request.user)
        except Company.DoesNotExist:
            raise NotFound("No company profile found. Please register first via /api/companies/register/.")

class CompanyViewSet(viewsets.ModelViewSet):
    """Full CRUD for Company profiles."""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "location"]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(detail=True, methods=["get"])
    def posts(self, request, pk=None):
        """GET /api/companies/{id}/posts/ — all posts for the company."""
        company = self.get_object()
        posts = company.posts.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    """CRUD for job posts with filtering, search and ordering."""
    queryset = Post.objects.select_related("company").all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["company", "onsite", "location"]
    search_fields = ["title", "position", "company__name", "requirement", "description"]
    ordering_fields = ["created_at", "salary", "min_year"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        # Force the post to belong to the current user's company
        user = self.request.user
        if not hasattr(user, "company_profile"):
            raise PermissionError("You must create a company profile first.")
        serializer.save(company=user.company_profile)

    def perform_update(self, serializer):
        # Ensure user owns the post via their company
        user = self.request.user
        if not hasattr(user, "company_profile"):
            raise PermissionError("You must create a company profile first.")
        if serializer.instance.company_id != user.company_profile.id:
            raise PermissionError(
                "You can only edit your own company's posts.")
        serializer.save()

    def get_permissions(self):
        # Anyone can read, only authed users can write
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        return PostCreateSerializer if self.action in ["create", "update", "partial_update"] else PostSerializer

    def perform_create(self, serializer):
        # Force the post to belong to the current user's company
        user = self.request.user
        if not hasattr(user, "company"):
            raise PermissionError("You must create a company profile first.")
        serializer.save(company=user.company)

    def perform_update(self, serializer):
        # Ensure user owns the post via their company
        user = self.request.user
        if not hasattr(user, "company"):
            raise PermissionError("You must create a company profile first.")
        # Optionally enforce ownership:
        if serializer.instance.company_id != user.company.id:
            raise PermissionError("You can only edit your own company's posts.")
        serializer.save()
        
    @action(detail=False, methods=["get"])
    def remote_jobs(self, request):
        posts = self.get_queryset().filter(onsite=False)
        return Response(self.get_serializer(posts, many=True).data)

    @action(detail=False, methods=["get"])
    def onsite_jobs(self, request):
        posts = self.get_queryset().filter(onsite=True)
        return Response(self.get_serializer(posts, many=True).data)

    @action(detail=False, methods=["get"])
    def by_salary_range(self, request):
        try:
            min_salary = int(request.query_params.get("min_salary", 0))
        except ValueError:
            min_salary = 0
        max_salary = request.query_params.get("max_salary")
        try:
            max_salary = int(max_salary) if max_salary is not None else None
        except ValueError:
            max_salary = None

        qs = self.get_queryset().filter(salary__gte=min_salary)
        if max_salary is not None:
            qs = qs.filter(salary__lte=max_salary)
        return Response(self.get_serializer(qs, many=True).data)


class StudentRegisterView(generics.CreateAPIView):
    """
    POST /api/students/register/
    Body (JSON):
      {
        "student_id": "6501234567",      # required
        "first_name": "Anna",            # optional
        "last_name": "Testi",            # optional
        "age": 22,                       # optional
        "nick_name": "Ann",              # optional
        "pronoun": "she/her"             # optional
      }

    Requirements:
    - Authorization: Bearer <access> (from /api/auth/google/)
    - Email is NOT accepted from the body; it is copied from request.user.email.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentRegisterSerializer
    queryset = Student.objects.all()


class StudentMeView(generics.RetrieveUpdateAPIView):
    """
    GET   /api/students/me/    -> current student profile
    PATCH /api/students/me/    -> partial update (first_name, last_name, age, etc.)
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSerializer

    def get_object(self):
        """Return current user's student profile or 404 if missing."""
        try:
            return Student.objects.get(user=self.request.user)
        except Student.DoesNotExist:
            raise NotFound("No student profile found. Please register first via /api/students/register/.")


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoint for listing and retrieving all students.
    - GET /api/students/      -> list all students
    - GET /api/students/{id}/ -> retrieve one student
    Permission: admin only (change if you want more public access).
    """
    queryset = Student.objects.select_related("user").all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]

# jobs/views.py (lisää loppuun)
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

from .models import Student, Company
from .serializers import UserPublicSerializer

class PendingStudentsListView(generics.ListAPIView):
    """
    GET /api/admin/students/pending/
    """
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return User.objects.filter(student_profile__is_approved=False)


class ApproveStudentView(APIView):
    """
    PATCH /api/admin/students/{user_id}/approve/
    Body: {"approve": true}
    """
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, user_id: int):
        approve = bool(request.data.get("approve", True))
        try:
            student = Student.objects.select_related("user").get(user__id=user_id)
        except Student.DoesNotExist:
            return Response({"detail": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        student.is_approved = approve
        student.save(update_fields=["is_approved"])
        return Response({
            "ok": True,
            "role": "student",
            "is_approved": student.is_approved,
            "user": UserPublicSerializer(student.user).data,
        })


class PendingCompaniesListView(generics.ListAPIView):
    """
    GET /api/admin/companies/pending/
    """
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return User.objects.filter(company_profile__is_approved=False)


class ApproveCompanyView(APIView):
    """
    PATCH /api/admin/companies/{user_id}/approve/
    Body: {"approve": true}
    """
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, user_id: int):
        approve = bool(request.data.get("approve", True))
        try:
            company = Company.objects.select_related("user").get(user__id=user_id)
        except Company.DoesNotExist:
            return Response({"detail": "Company not found."}, status=status.HTTP_404_NOT_FOUND)

        company.is_approved = approve
        company.save(update_fields=["is_approved"])
        return Response({
            "ok": True,
            "role": "company",
            "is_approved": company.is_approved,
            "user": UserPublicSerializer(company.user).data,
        })

class MeView(APIView):
    """
    GET /api/auth/me/
    Returns current user's public info + role + approval flag.
    """
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request):
        user = request.user
        data = UserPublicSerializer(user).data

        role, approved = None, None
        if hasattr(user, "student_profile"):
            role = "student"
            approved = user.student_profile.is_approved
        elif hasattr(user, "company_profile"):
            role = "company"
            approved = user.company_profile.is_approved

        data.update({"role": role, "is_approved": approved})
        return Response(data)

class EmailTokenObtainPairView(TokenViewBase):
    """
    POST /api/auth/login/
    Body: {"email":"...", "password":"..."}
    Returns: {"access":"...", "refresh":"..."}
    """
    serializer_class = EmailTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]