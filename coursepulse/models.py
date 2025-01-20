from django.db import models
from django.contrib.auth.models import User  # Assuming User is used for lecturers and students.

# LecturerCourse: Links lecturers to their assigned courses.
class LecturerCourse(models.Model):
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lecturer_courses")
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name="course_lecturers")
    assigned_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lecturer.username} - {self.course.name}"


# LecturerNotification: Logs notifications sent by lecturers.
class LecturerNotification(models.Model):
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lecturer_notifications")
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    level = models.CharField(max_length=10)  # Example: 100, 200, etc.
    department = models.CharField(max_length=100)  # Assuming a simple string for department.
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification by {self.lecturer.username} on {self.timestamp}"
