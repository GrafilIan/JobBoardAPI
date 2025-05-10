from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Custom User Model
class User(AbstractUser):
    is_employer = models.BooleanField(default=False)

    def __str__(self):
        role = "Employer" if self.is_employer else "Job Seeker"
        return f"{self.username} ({role})"

# Job Model
class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} - {self.location}"

# Application Model
class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(default=timezone.now)
    file_upload = models.FileField(upload_to='uploads/resume', null=True, blank=True)

    def __str__(self):
        return f"{self.applicant.username} applied to {self.job.title}"

