from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Course, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def schedule_course_notifications():
    """Schedule notifications for all courses in the next week"""
    users = User.objects.filter(role__in=['student', 'courserep'])
    
    for user in users:
        if not user.courses:  # Skip if user has no courses
            continue
            
        course_ids = user.courses
        courses = Course.objects.filter(id__in=course_ids)
        
        for course in courses:
            # Calculate next occurrence of this course
            today = timezone.now().date()
            days_ahead = {'MON': 0, 'TUE': 1, 'WED': 2, 'THU': 3, 'FRI': 4}
            days_until = days_ahead[course.day]
            
            if days_until < 0:  # If the day has passed this week
                days_until += 7  # Schedule for next week
                
            next_class = timezone.make_aware(
                timezone.datetime.combine(
                    today + timedelta(days=days_until),
                    course.start_time
                )
            )
            
            # Schedule start notification (5 minutes before class)
            start_notification_time = next_class - timedelta(minutes=5)
            Notification.objects.get_or_create(
                user=user,
                course=course,
                notification_type='START',
                scheduled_time=start_notification_time,
                is_sent=False
            )
            
            # Schedule end notification (5 minutes before end)
            end_time = timezone.make_aware(
                timezone.datetime.combine(
                    today + timedelta(days=days_until),
                    course.end_time
                )
            )
            end_notification_time = end_time - timedelta(minutes=5)
            Notification.objects.get_or_create(
                user=user,
                course=course,
                notification_type='END',
                scheduled_time=end_notification_time,
                is_sent=False
            )

@shared_task
def send_notifications():
    """Send pending notifications"""
    current_time = timezone.now()
    pending_notifications = Notification.objects.filter(
        is_sent=False,
        scheduled_time__lte=current_time
    )
    
    for notification in pending_notifications:
        # Here you would integrate with your actual notification service
        # (e.g., Firebase, email, SMS, etc.)
        print(f"Sending notification to {notification.user.email}: "
              f"{notification.course.code} is {'starting' if notification.notification_type == 'START' else 'ending'} "
              f"in 5 minutes")
        
        notification.is_sent = True
        notification.save()