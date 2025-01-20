from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
    ]

    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=3)
    faculty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    lecturer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'lecturer'}
    )

    def __str__(self):
        return f"{self.code} - {self.name}"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('START', 'Class Starting'),
        ('END', 'Class Ending'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=5, choices=NOTIFICATION_TYPES)
    scheduled_time = models.DateTimeField()
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'course', 'notification_type', 'scheduled_time']

    def __str__(self):
        return f"{self.user.username} - {self.course.code} - {self.notification_type}"
