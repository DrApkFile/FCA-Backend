from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import LecturerCourse, LecturerNotification, Course
from .serializers import LecturerNotificationSerializer
from django.conf import settings
from .models import Notification  # Assuming Notification is your existing notifications model.

class SendUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        course_id = data.get("course_id")
        level = data.get("level")
        department = data.get("department")
        message = data.get("message")

        # Validate input
        if not all([course_id, level, department, message]):
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(id=course_id)

            # Ensure the lecturer is authorized for the course
            if not LecturerCourse.objects.filter(course=course, lecturer=request.user).exists():
                return Response({"error": "Unauthorized action."}, status=status.HTTP_403_FORBIDDEN)

            # Create the notification in the database
            notification = LecturerNotification.objects.create(
                lecturer=request.user,
                course=course,
                level=level,
                department=department,
                message=message,
            )

            # Send email notifications
            self.send_emails(course, level, department, message)

            # Send app notifications
            self.send_app_notifications(course, level, department, message)

            return Response({"success": "Update sent successfully."}, status=status.HTTP_201_CREATED)
        except Course.DoesNotExist:
            return Response({"error": "Invalid course ID."}, status=status.HTTP_404_NOT_FOUND)

    def send_emails(self, course, level, department, message):
        """
        Sends email notifications to all students in the targeted course, level, and department.
        """
        # Assuming a `Student` model linked to a `Course` and having fields: `email`, `level`, `department`.
        from .models import Student  # Import the Student model.

        students = Student.objects.filter(
            courses=course, level=level, department=department
        )
        email_addresses = [student.email for student in students if student.email]

        if email_addresses:
            send_mail(
                subject=f"Update for {course.name}",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=email_addresses,
                fail_silently=False,
            )

    def send_app_notifications(self, course, level, department, message):
        """
        Sends app notifications to all students in the targeted course, level, and department.
        """
        # Assuming a `Student` model linked to `Notification`.
        from .models import Student  # Import the Student model.

        students = Student.objects.filter(
            courses=course, level=level, department=department
        )

        # Create a notification for each student
        notifications = [
            Notification(
                user=student.user,  # Assuming a `user` field in Student links to the User model
                title=f"Update for {course.name}",
                message=message,
            )
            for student in students
        ]

        # Bulk create notifications
        Notification.objects.bulk_create(notifications)
