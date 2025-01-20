from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()

class AttendanceLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey('timetable.Course', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    
    def is_expired(self):
        return timezone.now() >= self.expires_at
    
    def __str__(self):
        return f"{self.course.code} - {self.title}"

class AttendanceResponse(models.Model):
    attendance_link = models.ForeignKey(AttendanceLink, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    matric_number = models.CharField(max_length=20)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['attendance_link', 'matric_number']
    
    def __str__(self):
        return f"{self.matric_number} - {self.name}"

class AttendancePDF(models.Model):
    attendance_link = models.ForeignKey(AttendanceLink, on_delete=models.CASCADE)
    file = models.FileField(upload_to='attendance_pdfs/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Attendance PDF - {self.attendance_link.title}"