from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/', include('timetable.urls')),
    path('api/', include('tasks.urls')),
    path('api/', include('attendance.urls')),  
    path('api/', include('coursepulse.urls')),  
   
]