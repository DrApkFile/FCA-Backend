from rest_framework import serializers
from .models import Course, Notification

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'code', 'name', 'level', 'faculty', 'department', 
                 'day', 'start_time', 'end_time', 'lecturer']

class TimetableSerializer(serializers.Serializer):
    monday = CourseSerializer(many=True)
    tuesday = CourseSerializer(many=True)
    wednesday = CourseSerializer(many=True)
    thursday = CourseSerializer(many=True)
    friday = CourseSerializer(many=True)

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'course', 'notification_type', 'scheduled_time', 'is_sent']