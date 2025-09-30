"""
Domain models for the KUTechnest backend.

This app models three core entities:
- Company: an employer that can publish multiple job Posts.
- Post: a single job posting. It is linked to one Company and contains details like title,
        location, onsite/remote flag, salary, min years of experience, requirements and description.
        (Your project may also include optional fields such as `work_field` or `category`,
        and an `image_url` for a visual/logo.)
- Student: a student profile that can upload documents (CV, resume, transcript) via a safe path.

Notes
-----
- Timestamps (`created_at`, `updated_at`) are managed automatically.
- `student_file_upload_path` generates a unique, per-user subfolder and filename to avoid collisions.
"""
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import uuid
import os

# Possible location for company and post
POSSIBLE_LOCATIONS = [
     "bangkok", "chiang-mai", "chiang-rai", "lampang", "lamphun", "mae-hong-son",
    "nakhon-sawan", "nan", "phayao", "phetchabun", "phichit", "phitsanulok", "phrae",
    "sukhothai", "tak", "uthai-thani", "uttaradit", "chumphon", "krabi",
    "nakhon-si-thammarat", "narathiwat", "pattani", "phang-nga", "phatthalung",
    "phuket", "ranong", "satun", "songkhla", "surat-thani", "trang", "yala",
    "chachoengsao", "chanthaburi", "chonburi", "prachinburi", "rayong", "sa-kaeo",
    "trat", "amnat-charoen", "bueng-kan", "buriram", "chaiyaphum", "kalasin",
    "khon-kaen", "loei", "maha-sarakham", "mukdahan", "nakhon-phanom",
    "nakhon-ratchasima", "nong-bua-lamphu", "nong-khai", "roi-et", "sakon-nakhon",
    "sisaket", "surin", "ubon-ratchathani", "udon-thani", "yasothon", "ang-thong",
    "chai-nat", "kanchanaburi", "lopburi", "nakhon-nayok", "nakhon-pathom",
    "nonthaburi", "pathum-thani", "phra-nakhon-si-ayutthaya", "prachuap-khiri-khan",
    "ratchaburi", "samut-prakan", "samut-sakhon", "samut-songkhram", "saraburi",
    "sing-buri", "suphan-buri"
]
LOCATION_CHOICES = [(s, s.replace("-", " ").title()) for s in POSSIBLE_LOCATIONS]


EMPLOYMENT_CHOICES = [
        ("full_time", "Full time"),
        ("part_time", "Part time"),
        ("internship", "Internship"),
        ("contract", "Contract"),
    ]

class WorkField(models.TextChoices):
    """ Workfield for the search and the post """
    IT_SUPPORT     = "it-support", "IT Support / Helpdesk"
    CLOUD          = "cloud", "Cloud (AWS/GCP/Azure)"
    BACKEND        = "backend", "Backend Engineer"
    FRONTEND       = "frontend", "Frontend Developer"
    FULLSTACK      = "fullstack", "Full-stack Developer"
    DEVOPS         = "devops", "DevOps / Platform"
    QA             = "qa", "QA / Test Engineer"
    MOBILE         = "mobile", "Mobile Developer"
    DATA_ANALYST   = "data-analyst", "Data Analyst"
    DATA_ENGINEER  = "data-engineer", "Data Engineer"
    DATA_SCIENTIST = "data-scientist", "Data Scientist"
    AI_ML          = "ai-ml", "AI / ML"
    SECURITY       = "security", "Security / SecOps"
    NETWORK        = "network", "Network Engineer"
    SYSADMIN       = "sysadmin", "System Administrator"
    DATABASE       = "database", "Database / DBA"
    UI_UX          = "ui-ux", "UI/UX Designer"
    PRODUCT_DESIGN = "product-designer", "Product Designer"
    GAME_DEV       = "game-dev", "Game Developer"
    EMBEDDED       = "embedded", "Embedded / IoT"
    OTHER          = "other", "Other"

def student_file_upload_path(instance, filename):
    """Generate upload path for student files"""
    # Get file extension
    ext = filename.split('.')[-1]
    # Generate new filename with UUID
    filename = f"{uuid.uuid4()}.{ext}"
    # Return the upload path
    return os.path.join('student_files', str(instance.user.id), filename)


class Company(models.Model):
    """ Company that owns job posts."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
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
    """A student profile with personal and academic information."""
    # Personal info
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True, help_text="Full name")
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
    """ A single job posting published by company"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=300)
    work_field = models.CharField(
        max_length=32,
        choices=WorkField.choices,
        default=WorkField.OTHER,
        db_index=True,
    )

    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_CHOICES,
        default="full_time",
    )

    location = models.CharField(max_length=40, choices=LOCATION_CHOICES)
    onsite = models.BooleanField(default=False, help_text="True if onsite, False if remote")
    salary = models.IntegerField(help_text="Salary in your local currency")
    min_year = models.IntegerField(help_text="Minimum years of experience required")
    EMPLOYMENT_TYPE_CHOICES = [
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
    ]
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default="full_time"
    )
    requirement = models.TextField(help_text="Job requirements and qualifications")
    description = models.CharField(max_length=200, blank=True, default="")
    long_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True, null=True)
    long_description = models.TextField(blank=True, null=True, default="")
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} at {self.company.name}"
