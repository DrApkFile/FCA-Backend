from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.template.loader import render_to_string
from django.utils import timezone
from weasyprint import HTML
import tempfile
import os
from .models import AttendanceLink, AttendanceResponse, AttendancePDF
from .serializers import (
    AttendanceLinkSerializer,
    AttendanceResponseSerializer,
    AttendancePDFSerializer
)

class GenerateAttendanceLinkView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if request.user.role != 'courserep':
            return Response(
                {'error': 'Only course representatives can generate attendance links'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = AttendanceLinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubmitAttendanceView(views.APIView):
    def post(self, request, link_id):
        attendance_link = get_object_or_404(AttendanceLink, id=link_id)
        
        serializer = AttendanceResponseSerializer(
            data=request.data,
            context={'attendance_link': attendance_link}
        )
        
        if serializer.is_valid():
            serializer.save(attendance_link=attendance_link)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CancelAttendanceLinkView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, link_id):
        attendance_link = get_object_or_404(
            AttendanceLink,
            id=link_id,
            created_by=request.user
        )
        
        attendance_link.is_active = False
        attendance_link.save()
        
        return Response({'message': 'Attendance link cancelled successfully'})

class GenerateAttendancePDFView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, link_id):
        attendance_link = get_object_or_404(
            AttendanceLink,
            id=link_id,
            created_by=request.user
        )
        
        # Get all responses for this attendance link
        responses = AttendanceResponse.objects.filter(
            attendance_link=attendance_link
        ).order_by('submitted_at')
        
        # Generate PDF content
        html_string = render_to_string(
            'attendance/pdf_template.html',
            {
                'attendance_link': attendance_link,
                'responses': responses,
                'generated_at': timezone.now()
            }
        )
        
        # Create PDF using WeasyPrint
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_file:
            HTML(string=html_string).write_pdf(pdf_file.name)
            
            # Save PDF to database
            attendance_pdf = AttendancePDF.objects.create(
                attendance_link=attendance_link,
                file=pdf_file.name
            )
            
            return FileResponse(
                open(pdf_file.name, 'rb'),
                as_attachment=True,
                filename=f'attendance_{attendance_link.id}.pdf'
            )

class ListAttendancePDFsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendancePDFSerializer
    
    def get_queryset(self):
        return AttendancePDF.objects.filter(
            attendance_link__created_by=self.request.user
        ).order_by('-created_at')