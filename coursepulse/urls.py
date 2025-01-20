from django.urls import path
from .views import LecturerCoursesView, SendUpdateView

urlpatterns = [
    path('lecturer/courses/', LecturerCoursesView.as_view(), name='lecturer-courses'),
    path('lecturer/send-update/', SendUpdateView.as_view(), name='send-update'),
]
