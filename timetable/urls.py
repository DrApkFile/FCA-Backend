from django.urls import path
from .views import TimetableView

urlpatterns = [
    path('timetable/', TimetableView.as_view(), name='timetable'),
]