# jobs/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Student, Company

# Optional: restrict student emails to KU domains (edit or set to empty set to disable)
ALLOWED_STUDENT_EMAIL_DOMAINS = {"ku.th", "live.ku.th"}


class UserPublicSerializer(serializers.ModelSerializer):
    """
    Minimal public representation of Django's User.
    Useful for embedding user info inside student/company responses.
    """
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "username"]


# ----------------------------
# Student Registration
# ----------------------------
class StudentRegisterSerializer(serializers.Serializer):
    """
    Creates a new User and links it to a Student profile.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    age = serializers.IntegerField(required=False, min_value=0)
    major = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        """
        Ensure uniqueness and (optionally) enforce KU domains.
        """
        domain = value.split("@")[-1].lower()
        if ALLOWED_STUDENT_EMAIL_DOMAINS and domain not in ALLOWED_STUDENT_EMAIL_DOMAINS:
            raise serializers.ValidationError("Only KU student emails are allowed.")
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def create(self, validated_data):
        """
        Create User first (username=email), then the Student profile.
        """
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        first_name = validated_data.pop("first_name", "")
        last_name = validated_data.pop("last_name", "")

        user = User.objects.create_user(
            username=email,  # set username=email so default auth works
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        student = Student.objects.create(user=user, is_approved=False, **validated_data)
        return student

    def to_representation(self, instance: Student):
        """
        How the API returns a student after registration.
        """
        base = UserPublicSerializer(instance.user).data
        base.update({
            "role": "student",
            "is_approved": instance.is_approved,
            "age": instance.age,
            "major": instance.major,
        })
        return base


# ----------------------------
# Company Registration
# ----------------------------
class CompanyRegisterSerializer(serializers.Serializer):
    """
    Creates a new User and links it to a Company profile.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    name = serializers.CharField()
    website = serializers.URLField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        """
        Ensure uniqueness (no domain restriction for companies by default).
        """
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def create(self, validated_data):
        """
        Create User first (username=email), then the Company profile.
        """
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        first_name = validated_data.pop("first_name", "")
        last_name = validated_data.pop("last_name", "")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        company = Company.objects.create(user=user, is_approved=False, **validated_data)
        return company

    def to_representation(self, instance: Company):
        """
        How the API returns a company after registration.
        """
        base = UserPublicSerializer(instance.user).data
        base.update({
            "role": "company",
            "is_approved": instance.is_approved,
            "name": instance.name,
            "website": instance.website,
            "location": instance.location,
            "description": instance.description,
        })
        return base


# ----------------------------
# Email-based JWT Login
# ----------------------------
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Allows login with {"email": "...", "password": "..."}.
    Internally maps email -> username so we can reuse the default auth flow.
    """
    email = serializers.EmailField(write_only=True)

    def __init__(self, *args, **kwargs):
        """
        Remove 'username' from required fields since we take 'email' instead.
        """
        super().__init__(*args, **kwargs)
        self.fields.pop("username", None)

    def validate(self, attrs):
        """
        Convert provided email to the corresponding username, then call parent validate.
        """
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "No user found with this email."})

        attrs["username"] = user.username
        attrs["password"] = password

        # This returns the standard SimpleJWT payload: access, refresh, etc.
        data = super().validate(attrs)
        return data

# --- Minimal stubs to satisfy existing imports in jobs/views.py ---


class CompanySerializer(serializers.ModelSerializer):
    """
    Minimal serializer so that existing views importing CompanySerializer won't crash.
    Adjust fields to your real needs later.
    """
    class Meta:
        model = Company
        fields = ["id", "name", "website", "location", "description", "is_approved", "user"]


class StudentSerializer(serializers.ModelSerializer):
    """
    Minimal serializer for student profiles used by older views.
    """
    # Show minimal user info if you like:
    # user = UserPublicSerializer(read_only=True)
    class Meta:
        model = Student
        fields = ["id", "age", "major", "is_approved", "user"]


# If your views import PostSerializer / PostCreateSerializer, provide light versions too.
# These fields are guesses; adjust to match your Post model.
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "company", "company_name", "title", "work_field", "location",
            "onsite", "salary", "min_year", "requirement", "description",
            "image_url", "created_at", "updated_at", "employment_type"
        ]
        read_only_fields = ["id", "company_name", "created_at", "updated_at"]


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "title", "work_field", "location", "onsite", "salary", "min_year",
            "requirement", "description", "image_url", "employment_type"
        ]
