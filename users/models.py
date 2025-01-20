# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('course_rep', 'Course Rep'),
        ('lecturer', 'Lecturer'),
    )
    level = models.CharField(max_length=10, blank=True, null=True)  # e.g., "100", "200", etc.
    faculty = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    courses = models.ManyToManyField('Course', blank=True)  # Assuming you have a Course model
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    pin = models.CharField(max_length=10, blank=True, null=True)  # Only used for Course Rep and Lecturer

    def __str__(self):
        return self.username


class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    additional_info = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
