from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task, TaskNotification
from .serializers import TaskSerializer, TaskNotificationSerializer
from datetime import timedelta
from django.utils import timezone

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        task = serializer.save(user=self.request.user)
        self._schedule_notifications(task)

    def perform_update(self, serializer):
        task = serializer.save()
        # Delete existing notifications and reschedule
        TaskNotification.objects.filter(task=task).delete()
        self._schedule_notifications(task)

    def perform_destroy(self, instance):
        # Delete associated notifications before deleting task
        TaskNotification.objects.filter(task=instance).delete()
        instance.delete()

    def _schedule_notifications(self, task):
        # Schedule start notification (5 minutes before)
        TaskNotification.objects.create(
            user=self.request.user,
            task=task,
            notification_type='START',
            scheduled_time=task.start_time - timedelta(minutes=5)
        )

        # Schedule end notification (5 minutes before)
        TaskNotification.objects.create(
            user=self.request.user,
            task=task,
            notification_type='END',
            scheduled_time=task.end_time - timedelta(minutes=5)
        )

tott
titwuwa
auvsiai
avsiubis
auius








