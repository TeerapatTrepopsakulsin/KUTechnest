"""DRF serializers that define the public JSON shape of the API."""
from rest_framework import serializers
from .models import Company, Post


class CompanySerializer(serializers.ModelSerializer):
    """Public representation of a Company."""
    posts_count = serializers.SerializerMethodField()
    class Meta:
        model = Company
        fields = ['id', 'name', 'website', 'location', 'description',
                  'created_at', 'updated_at', 'logo_url', 'posts_count']

    def get_posts_count(self, obj):
        return obj.posts.count()


class PostSerializer(serializers.ModelSerializer):
    """Read serializer for Post (used for GET/list/retrieve)"""
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'company', 'company_name', 'title', 'work_field',
                  'location', 'onsite', 'salary', 'min_year', 'requirement',
                  'description','image_url',  'created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            data['salary'] = f"{int(instance.salary):,}"
        except Exception:
            pass
        if 'image_url' in data and not data.get('image_url'):
            company_logo = getattr(getattr(instance, 'company', None),
                                   'logo_url', None)
            if company_logo:
                data['image_url'] = company_logo
        return data


class PostCreateSerializer(serializers.ModelSerializer):
    """Separate serializer for creating posts with company validation"""

    class Meta:
        model = Post
        fields = ['company', 'title', 'work_field', 'location', 'onsite',
                  'salary', 'min_year', 'requirement', 'description' ]

    def validate_salary(self, value):
        if value <= 0:
            raise serializers.ValidationError("Salary must be greater than 0")
        return value

    def validate_min_year(self, value):
        if value < 0:
            raise serializers.ValidationError("Minimum years cannot be negative")
        return value
