from django.urls import path
from .views import (
    GenerateAttendanceLinkView,
    SubmitAttendanceView,
    CancelAttendanceLinkView,
    GenerateAttendancePDFView,
    ListAttendancePDFsView
)

urlpatterns = [
    path('attendance/generate/', 
         GenerateAttendanceLinkView.as_view(),
         name='generate-attendance'),
    path('attendance/<uuid:link_id>/submit/',
         SubmitAttendanceView.as_view(),
         name='submit-attendance'),
    path('attendance/<uuid:link_id>/cancel/',
         CancelAttendanceLinkView.as_view(),
         name='cancel-attendance'),
    path('attendance/<uuid:link_id>/pdf/',
         GenerateAttendancePDFView.as_view(),
         name='generate-pdf'),
    path('attendance/pdfs/',
         ListAttendancePDFsView.as_view(),
         name='list-pdfs'),
]