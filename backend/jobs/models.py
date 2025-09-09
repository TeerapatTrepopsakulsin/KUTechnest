from django.contrib.auth.models import User
from django.db import models
import uuid
import os


def student_file_upload_path(instance, filename):
    """Generate upload path for student files with a UUID filename"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("student_files", str(instance.user.id), filename)


class Company(models.Model):
    """Company profile linked 1:1 to a User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    contacts = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Student(models.Model):
    """Student profile linked 1:1 to a User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Optional basic name info at registration
    first_name = models.CharField(max_length=150, blank=True, default="")
    last_name  = models.CharField(max_length=150, blank=True, default="")

    # REQUIRED for registration
    student_id = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        blank=False,
        help_text="KU student ID number"
    )

    # Optional personal info
    nick_name = models.CharField(max_length=30, null=True, blank=True, help_text="Preferred nickname")
    pronoun   = models.CharField(max_length=20, null=True, blank=True)
    age       = models.PositiveIntegerField(null=True, blank=True)

    # Academic info (optional initially; can be filled later)
    year          = models.PositiveSmallIntegerField(null=True, blank=True)
    ku_generation = models.PositiveSmallIntegerField(null=True, blank=True)
    faculty       = models.CharField(max_length=100, null=True, blank=True)
    major         = models.CharField(max_length=100, null=True, blank=True)
    about_me      = models.TextField(blank=True, default="", help_text="Tell us about yourself")

    # Contact info (taken from request.user.email during registration)
    email = models.EmailField(help_text="Contact email address")

    # File uploads (optional)
    cv         = models.FileField(upload_to=student_file_upload_path, blank=True, null=True)
    resume     = models.FileField(upload_to=student_file_upload_path, blank=True, null=True)
    transcript = models.FileField(upload_to=student_file_upload_path, blank=True, null=True)

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        full = (self.first_name + " " + self.last_name).strip()
        return f"{full or self.user.username} ({self.student_id})"


class Post(models.Model):
    """Job post created by a company"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=300)
    position = models.CharField(max_length=120, blank=True, default="")
    work_field = models.CharField(max_length=120, blank=True, default="")
    employment_type = models.CharField(max_length=50, blank=True, default="")
    location = models.CharField(max_length=200)
    onsite = models.BooleanField(default=False, help_text="True if onsite, False if remote")
    salary = models.IntegerField(help_text="Salary in your local currency")
    min_year = models.IntegerField(help_text="Minimum years of experience required")
    requirement = models.TextField(help_text="Job requirements and qualifications")
    description = models.TextField(help_text="Detailed job description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True, default="")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.position} at {self.company.name}"
