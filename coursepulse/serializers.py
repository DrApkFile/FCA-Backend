from rest_framework import serializers
from .models import LecturerCourse, LecturerNotification
from .models import Course  # Assuming existing Course model.

class LecturerCourseSerializer(serializers.ModelSerializer):
    course_name = serializers.ReadOnlyField(source="course.name")

    class Meta:
        model = LecturerCourse
        fields = ['id', 'lecturer', 'course', 'course_name', 'assigned_date']


class LecturerNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturerNotification
        fields = ['id', 'lecturer', 'course', 'level', 'department', 'message', 'timestamp']
