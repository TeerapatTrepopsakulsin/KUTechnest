from django.contrib import admin
from .models import Company, Post, Student


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'posts_count', 'created_at')
    list_filter = ('location', 'created_at')
    search_fields = ('name', 'location')
    readonly_fields = ('created_at', 'updated_at')

    def posts_count(self, obj):
        return obj.posts.count()

    posts_count.short_description = 'Number of Posts'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'position', 'location', 'onsite', 'salary', 'min_year', 'created_at')
    list_filter = ('onsite', 'company', 'location', 'min_year', 'created_at')
    search_fields = ('title', 'position', 'company__name', 'requirement', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('onsite', 'salary')

    fieldsets = (
        ('Basic Information', {
            'fields': ('company', 'title', 'position')
        }),
        ('Job Details', {
            'fields': ('location', 'onsite', 'salary', 'min_year')
        }),
        ('Job Content', {
            'fields': ('requirement', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
