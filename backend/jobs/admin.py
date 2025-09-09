from django.contrib import admin
from django.utils.html import format_html
from .models import Company, Post, Student


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('logo_thumb', 'name', 'location', 'posts_count',
                    'created_at')
    list_filter = ('location', 'created_at')
    search_fields = ('name', 'location')
    readonly_fields = ('created_at', 'updated_at')

    def posts_count(self, obj):
        return obj.posts.count()

    def logo_thumb(self, obj):
        if obj.logo_url:
            return format_html(
                '<img src="{}" width="48" height="48" style='
                '"object-fit:contain;background:#fff;border-radius:6px;'
                'padding:4px;" />',
                obj.logo_url
            )
        return "—"
    logo_thumb.short_description = "Logo"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('logo', 'title', 'company', 'location', 'onsite',
                    'employment_type',
                    'salary', 'min_year', 'created_at',
                    )
    list_filter = ('onsite', 'company', 'location', 'min_year', 'created_at')
    search_fields = ('title', 'company__name', 'requirement', 'description',
                     )
    readonly_fields = ('created_at', 'updated_at')

    def logo(self, obj):
        url = getattr(obj.company, 'logo_url', None)
        if url:
            return format_html(
                '<img src="{}" width="40" height="40" style="object-fit'
                ':contain;border-radius:6px;background:#fff;padding:3px;" />',
                url
            )
        return "—"
    logo.short_description = "Logo"

    def get_fieldsets(self, request, obj=None):
        basic = ['company', 'title']
        if hasattr(Post, 'work_field'):
            basic.append('work_field')
        if hasattr(Post, 'image_url'):
            basic.append('image_url')
        return (
            ('Basic Information', {'fields': tuple(basic)}),
            ('Job Details', {'fields': ('location', 'onsite', 'salary',
                                        'min_year','employment_type',
                                        'description')}),
            ('Job Content', {'fields': ('long_description','requirement')}),
            ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
        )
