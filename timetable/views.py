from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Course
from .serializers import TimetableSerializer
from collections import defaultdict

class TimetableView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.role not in ['student', 'courserep']:
            return Response(
                {'error': 'Only students and course reps can view timetables'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not request.user.courses:
            return Response(
                {'error': 'No courses selected'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get user's courses
        courses = Course.objects.filter(id__in=request.user.courses)
        
        # Organize courses by day
        timetable = defaultdict(list)
        for course in courses:
            day_map = {
                'MON': 'monday',
                'TUE': 'tuesday',
                'WED': 'wednesday',
                'THU': 'thursday',
                'FRI': 'friday'
            }
            timetable[day_map[course.day]].append(course)
        
        # Ensure all days are included in response
        formatted_timetable = {
            'monday': timetable['monday'],
            'tuesday': timetable['tuesday'],
            'wednesday': timetable['wednesday'],
            'thursday': timetable['thursday'],
            'friday': timetable['friday']
        }
        
        serializer = TimetableSerializer(formatted_timetable)
        return Response(serializer.data)