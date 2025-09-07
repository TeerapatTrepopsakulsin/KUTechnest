
from .models import Company, Post
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # we’ll accept email + password; we'll store username=email
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        email = validated_data["email"].lower().strip()
        password = validated_data["password"]
        first_name = validated_data.get("first_name", "")
        last_name = validated_data.get("last_name", "")

        user = User(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save()
        return user


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


class PostListSerializer(serializers.ModelSerializer):
    # serializer for listing posts (short card view)
    company_name = serializers.CharField(source="company.name", read_only=True)

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
