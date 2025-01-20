import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ai'))
from django.urls import path
from . import views
from ai import api  # Importing from the ai folder

urlpatterns = [
    # Views for handling various tasks
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('course_summary/<int:course_id>/', views.course_summary, name='course_summary'),
    path('summarize_youtube/', views.summarize_youtube, name='summarize_youtube'),
    path('fine_tune/', views.fine_tune, name='fine_tune'),
    path('chatbot/', views.general_knowledge_chat, name='general_knowledge_chat'),
    
    # API routes for interacting with the LLM (from ai/api.py)
    path('generate_response/', api.generate_response, name='generate_response'),
    path('summarize_text/', api.summarize_text, name='summarize_text'),
    path('fine_tune/', api.fine_tune, name='fine_tune'),
]
