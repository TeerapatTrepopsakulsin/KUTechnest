from rest_framework import serializers
from .models import Company, Post


class CompanySerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'website', 'location', 'description',
                  'created_at', 'updated_at', 'posts_count']

    def get_posts_count(self, obj):
        return obj.posts.count()


class PostSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'company', 'company_name', 'title', 'position',
                  'location', 'onsite', 'salary', 'min_year', 'requirement',
                  'description', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Format salary with commas for better readability
        representation['salary'] = f"{instance.salary:,}"
        return representation


class PostCreateSerializer(serializers.ModelSerializer):
    """Separate serializer for creating posts with company validation"""

    class Meta:
        model = Post
        fields = ['company', 'title', 'position', 'location', 'onsite',
                  'salary', 'min_year', 'requirement', 'description']

    def validate_salary(self, value):
        if value <= 0:
            raise serializers.ValidationError("Salary must be greater than 0")
        return value

    def validate_min_year(self, value):
        if value < 0:
            raise serializers.ValidationError("Minimum years cannot be negative")
        return value
