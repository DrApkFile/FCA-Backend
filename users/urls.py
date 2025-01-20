# urls.py

from django.urls import path
from .views import SignupView, LoginView, ForgotPasswordView, ResetPasswordView, LecturerSignupView, LogoutView, UserInfoView, ChangeUsernameView, ChangePasswordView, DeleteAccountView

urlpatterns = [
    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('api/reset-password/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),
    path('api/logout/', LogoutView.as_view(), name='logout'),  
    path('api/user-info/', UserInfoView.as_view(), name='user-info'),  
    path('api/change-username/', ChangeUsernameView.as_view(), name='change-username'),  
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),  
    path('api/delete-account/', DeleteAccountView.as_view(), name='delete-account'),  
]
