# views.py

from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from .models import Lecturer

# Signup Serializer for handling user registration
class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'level', 'faculty', 'department', 'courses', 'email', 'password', 'role', 'pin']

    def validate(self, attrs):
        role = attrs.get('role')

        # If Course Rep or Lecturer, validate pin
        if role in ['course_rep', 'lecturer']:
            pin = attrs.get('pin')
            if role == 'course_rep' and pin != '12345': # will still add an array for different pins once i confirm from school
                raise serializers.ValidationError("Invalid PIN for Course Rep.")
            elif role == 'lecturer' and pin != '56789':
                raise serializers.ValidationError("Invalid PIN for Lecturer.")

        # If Lecturer and email already exists, update lecturer info
        if role == 'lecturer' and User.objects.filter(email=attrs.get('email')).exists():
            user = User.objects.get(email=attrs.get('email'))
            user.username = attrs.get('username')
            user.password = attrs.get('password')  # Ensure proper hashing
            user.save()
            return user

        return attrs

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login Serializer for handling user authentication
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = authenticate(username=username, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=200)
            return Response({"error": "Invalid credentials"}, status=400)
        return Response(serializer.errors, status=400)


# Forgot Password View
class ForgotPasswordView(APIView):
    def post(self, request):
        username_or_email = request.data.get("username_or_email")
        try:
            user = User.objects.get(username=username_or_email) if "@" not in username_or_email else User.objects.get(email=username_or_email)
            token = get_random_string(length=32)
            reset_link = f"http://example.com/reset-password/{token}/"
            
            # Save the reset token and expiration date
            user.reset_token = token
            user.reset_token_expiry = timezone.now() + timedelta(minutes=15)
            user.save()

            # Send reset link to email
            send_mail("Password Reset", f"Click the link to reset your password: {reset_link}", "admin@example.com", [user.email])

            return Response({"message": "Reset link sent to email."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# Reset Password View
class ResetPasswordView(APIView):
    def post(self, request, token):
        new_password = request.data.get("new_password")

        # Find the user by the reset token
        try:
            user = User.objects.get(reset_token=token)

            if timezone.now() > user.reset_token_expiry:
                return Response({"error": "Reset token has expired."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.reset_token = None
            user.reset_token_expiry = None
            user.save()

            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


# User Management APIs

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'role']

class UserInfoView(APIView):
    """Fetch user info (Username, Email, Role)."""
    def get(self, request):
        user = request.user
        serializer = UserInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangeUsernameSerializer(serializers.Serializer):
    new_username = serializers.CharField(max_length=150)

    def validate_new_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

class ChangeUsernameView(APIView):
    """Change username of the user."""
    def post(self, request):
        serializer = ChangeUsernameSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            user.username = serializer.validated_data['new_username']
            user.save()
            return Response({"message": "Username updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        user = self.context['request'].user
        current_password = data.get('current_password')
        
        # Check if the current password is correct
        if not user.check_password(current_password):
            raise serializers.ValidationError("Current password is incorrect.")
        return data


class ChangePasswordView(APIView):
    """Change the user's password."""
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)  # Update session to keep user logged in
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountSerializer(serializers.Serializer):
    confirm_deletion = serializers.BooleanField()

    def validate_confirm_deletion(self, value):
        if not value:
            raise serializers.ValidationError("You must confirm account deletion.")
        return value


class DeleteAccountView(APIView):
    """Delete user's account after confirmation."""
    def post(self, request):
        serializer = DeleteAccountSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            # Perform deletion
            user.delete()
            return Response({"message": "Account deleted successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Logout View
class LogoutView(APIView):
    def post(self, request):
        try:
            # Get the token from the request header
            token = request.headers.get('Authorization').split(' ')[1]  # "Bearer <token>"
            user_token = Token.objects.get(key=token)
            
            # Delete the token to log the user out
            user_token.delete()
            
            return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
        
        except (Token.DoesNotExist, IndexError):
            return Response({"error": "Invalid or missing token."}, status=status.HTTP_400_BAD_REQUEST)
