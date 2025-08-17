from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import uuid
import os


def student_file_upload_path(instance, filename):
    """Generate upload path for student files"""
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate new filename with UUID
    filename = f"{uuid.uuid4()}.{ext}"
    # Return the upload path
    return os.path.join('student_files', str(instance.user.id), filename)


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    contacts = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, help_text="Full name")
    nick_name = models.CharField(max_length=30, null=True, blank=True, help_text="Preferred nickname")
    pronoun = models.CharField(max_length=20, null=True, blank=True)
    age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(15), MaxValueValidator(100)],
        help_text="Age in years"
    )
    # Academic info
    year = models.PositiveSmallIntegerField()
    ku_generation = models.PositiveSmallIntegerField()
    faculty = models.CharField(max_length=100, )
    major = models.CharField(max_length=100, null=True, blank=True)
    about_me = models.TextField(blank=True, help_text="Tell us about yourself")

    # Personal info
    email = models.EmailField(help_text="Contact email address")

    # File uploads
    cv = models.FileField(
        upload_to=student_file_upload_path,
        blank=True,
        null=True,
        help_text="Upload your CV (PDF recommended)"
    )
    resume = models.FileField(
        upload_to=student_file_upload_path,
        blank=True,
        null=True,
        help_text="Upload your resume (PDF recommended)"
    )
    transcript = models.FileField(
        upload_to=student_file_upload_path,
        blank=True,
        null=True,
        help_text="Upload your academic transcript (PDF recommended)"
    )


class Post(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=300)
    position = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    onsite = models.BooleanField(default=False, help_text="True if onsite, False if remote")
    salary = models.IntegerField(help_text="Salary in your local currency")
    min_year = models.IntegerField(help_text="Minimum years of experience required")
    requirement = models.TextField(help_text="Job requirements and qualifications")
    description = models.TextField(help_text="Detailed job description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.position} at {self.company.name}"
