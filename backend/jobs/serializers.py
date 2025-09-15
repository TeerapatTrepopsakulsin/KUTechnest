from django.contrib.auth import get_user_model
from rest_framework import serializers, exceptions
from .models import Company, Post, Student
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

DEFAULT_IMG = "https://placehold.co/200x200?text=KU+TechNest"


class CompanySerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = [
            "id", "name", "website", "location", "description",
            "created_at", "updated_at", "logo_url", "posts_count",
        ]

    def get_posts_count(self, obj):
        return obj.posts.count()


class CompanyRegisterSerializer(serializers.ModelSerializer):
    """If you create companies via API (without touching the related user here)."""
    class Meta:
        model = Company
        fields = ["name", "website", "location", "description", "contacts", "logo_url"]


class PostSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)
    company_logo = serializers.CharField(source="company.logo_url", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "company", "company_name",
            "title", "work_field", "employment_type",
            "location", "onsite", "salary", "min_year",
            "requirement", "description",
            "long_description",
            "company_logo",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "company_name", "company_logo"]


class PostListSerializer(serializers.ModelSerializer):
    # serializer for listing posts (short card view)
    company_name = serializers.CharField(source="company.name", read_only=True)
    image_url = serializers.SerializerMethodField()

    def get_company_logo(self, obj):
        return (getattr(obj.company, "logo_url", "") or DEFAULT_IMG)

    def get_image_url(self, obj):
        # prefer post image, else company logo, else placeholder
        return (obj.image_url or getattr(obj.company, "logo_url",
                                         "") or DEFAULT_IMG)

    class Meta:
        model = Post
        fields = [
            "id", "company", "company_name", "title", "work_field",
            "location","employment_type", "onsite", "salary", "min_year",
            "requirement",
            "description", "image_url", "created_at", "updated_at",

        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            data["salary"] = f"{int(instance.salary):,}"
        except Exception:
            pass
        if not data.get("image_url"):
            company_logo = getattr(getattr(instance, "company", None), "logo_url", None)
            if company_logo:
                data["image_url"] = company_logo
        return data


class PostDetailSerializer(PostListSerializer):
    # adds long_description for detail view
    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ["long_description"]


class PostCreateSerializer(serializers.ModelSerializer):
    # serializer for create/update
    class Meta:
        model = Post
        fields = [
            "company", "title", "work_field", "description",
            "location", "onsite", "salary", "min_year",
            "long_description", "requirement", "image_url",
            "employment_type",
        ]

    def validate_salary(self, value):
        if value <= 0:
            raise serializers.ValidationError("Salary must be greater than 0")
        return value

    def validate_min_year(self, value):
        if value < 0:
            raise serializers.ValidationError("Minimum years cannot be negative")
        return value

    def validate(self, attrs):
        # ensure description is always filled
        if not (attrs.get("description") or "").strip() and (attrs.get("long_description") or "").strip():
            attrs["description"] = attrs["long_description"]
        return attrs


class PostListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "company", "company_name", "title", "work_field",
            "location", "employment_type", "onsite", "salary", "min_year",
            "requirement", "description", "image_url",
            "created_at", "updated_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Format salary safely whether it's int/Decimal/"15,000"/"15 000"
        raw = getattr(instance, "salary", None)
        if raw is not None:
            try:
                # keep only digits before casting (handles "15,000", "15 000")
                digits = "".join(ch for ch in str(raw) if ch.isdigit())
                if digits:
                    data["salary"] = f"{int(digits):,}"
            except Exception:
                pass

        # Fallback logo
        if not data.get("image_url"):
            company_logo = getattr(getattr(instance, "company", None), "logo_url", None)
            if company_logo:
                data["image_url"] = company_logo
        return data


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"   # or list fields explicitly if you prefer


class StudentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "user", "name", "nick_name", "pronoun", "age",
            "year", "ku_generation", "faculty", "major",
            "about_me", "email",
            "cv", "resume", "transcript",
        ]

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]
        read_only_fields = fields


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Login with email + password.
    Returns refresh, access and basic user data.
    """

    username_field = "email"

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise exceptions.AuthenticationFailed("Email and password required")

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid credentials")

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Invalid credentials")

        if not user.is_active:
            raise exceptions.AuthenticationFailed("User is inactive")

        refresh = self.get_token(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        }