from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import TaskNotification

@shared_task
def send_task_notifications():
    """Send pending task notifications via email"""
    current_time = timezone.now()
    
    # Fetch pending notifications scheduled to be sent
    pending_notifications = TaskNotification.objects.filter(
        is_sent=False,
        scheduled_time__lte=current_time
    ).select_related('user', 'task')
    
    for notification in pending_notifications:
        # Define the action based on notification type
        action = 'starting' if notification.notification_type == 'START' else 'ending'
        
        # Construct the message to send
        message = f"Dear {notification.user.first_name},\n\n" \
                  f"Task '{notification.task.name}' is {action} in 5 minutes.\n" \
                  f"Please be ready for the task.\n\nBest regards,\nTask Manager Team"

        # Send the email notification
        send_mail(
            subject=f"Task '{notification.task.name}' - {action} in 5 minutes",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,  # The default sender email
            recipient_list=[notification.user.email],
            fail_silently=False,
        )

        # Log that the notification has been sent
        notification.is_sent = True
        notification.save()

        print(f"Sent task notification to {notification.user.email}: "
              f"Task '{notification.task.name}' is {action} in 5 minutes.")
