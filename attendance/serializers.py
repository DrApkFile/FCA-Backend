from rest_framework import serializers
from .models import AttendanceLink, AttendanceResponse, AttendancePDF
from django.utils import timezone
from datetime import timedelta

class AttendanceLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceLink
        fields = ['id', 'course', 'title', 'created_at', 'expires_at', 'is_active']
        read_only_fields = ['id', 'created_at', 'expires_at', 'is_active']
    
    def create(self, validated_data):
        # Set expiration time to 15 minutes from now
        validated_data['expires_at'] = timezone.now() + timedelta(minutes=15)
        return super().create(validated_data)

class AttendanceResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceResponse
        fields = ['id', 'name', 'matric_number', 'submitted_at']
        read_only_fields = ['id', 'submitted_at']
    
    def validate(self, data):
        attendance_link = self.context['attendance_link']
        
        if attendance_link.is_expired() or not attendance_link.is_active:
            raise serializers.ValidationError("This attendance link has expired or is inactive")
        
        # Check if matric number already submitted
        if AttendanceResponse.objects.filter(
            attendance_link=attendance_link,
            matric_number=data['matric_number']
        ).exists():
            raise serializers.ValidationError("You have already submitted attendance")
        
        return data

class AttendancePDFSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendancePDF
        fields = ['id', 'file', 'created_at']
        read_only_fields = ['id', 'file', 'created_at']