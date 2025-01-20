import os
import re
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import UploadedFile, Course, YouTubeLink
from .tasks import fine_tune_model
from .pdf_summary import summarize_pdf
from .course_summary import summarize_course
from .youtube_summary import summarize_youtube
from youtube_transcript_api import YouTubeTranscriptApi
from django.conf import settings

# View to handle PDF upload and summarization
def upload_pdf(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        pdf_instance = UploadedFile.objects.create(file=uploaded_file)
        
        # Trigger PDF summarization
        summarize_pdf(pdf_instance.id)
        
        return JsonResponse({'status': 'PDF uploaded successfully, summarization in progress.'}, status=200)
    
    return JsonResponse({'error': 'Invalid request method. POST required.'}, status=400)

# View for course summarization
def course_summary(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Get the course topics and materials and display them
    summary = summarize_course(course)  # Custom function to summarize course
    return JsonResponse({'course': course.title, 'summary': summary}, status=200)

# View to handle YouTube link submission and summarization
def summarize_youtube(request):
    if request.method == 'POST':
        url = request.POST['youtube_link']
        video_id = extract_video_id(url)  # Extract video ID from the URL
        
        if not video_id:
            return JsonResponse({'error': 'Invalid YouTube URL'}, status=400)
        
        # Get the transcript for the YouTube video
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        # Create a new entry for YouTubeLink
        link_instance = YouTubeLink.objects.create(url=url, transcript=transcript)
        
        # Use the YouTube transcript for further processing (summarization)
        summary = summarize_youtube(link_instance)
        
        return JsonResponse({'url': url, 'transcript': transcript, 'summary': summary}, status=200)
    
    return JsonResponse({'error': 'Invalid request method. POST required.'}, status=400)

# Helper function to extract YouTube video ID from URL
def extract_video_id(url):
    video_id_match = re.match(r'https://www\.youtube\.com/watch\?v=([a-zA-Z0-9_-]+)', url)
    if video_id_match:
        return video_id_match.group(1)
    return None

# View to trigger the fine-tuning process
def fine_tune(request):
    if request.method == 'POST':
        # Trigger the fine-tuning task
        fine_tune_model.delay()  # Using Celery to run the task asynchronously
        
        return JsonResponse({'status': 'Fine-tuning process started'}, status=200)
    
    return JsonResponse({'error': 'Invalid request method. POST required.'}, status=400)

# General Knowledge Chatbot View
def general_knowledge_chat(request):
    if request.method == 'POST':
        user_input = request.POST['user_input']
        
        # Here, we should call the trained GPT-2 model to generate a response
        # Assuming you have some function `generate_response_from_model` that queries the model
        response = generate_response_from_model(user_input)
        
        return JsonResponse({'response': response}, status=200)
    
    return JsonResponse({'error': 'Invalid request method. POST required.'}, status=400)

# Helper function for generating a response from GPT-2 (you'd implement this using the fine-tuned model)
def generate_response_from_model(user_input):
    from transformers import GPT2Tokenizer, TFGPT2LMHeadModel

    tokenizer = GPT2Tokenizer.from_pretrained('chatbot/ai/fine_tuned_model')
    model = TFGPT2LMHeadModel.from_pretrained('chatbot/ai/fine_tuned_model')

    inputs = tokenizer.encode(user_input, return_tensors='tf')
    outputs = model.generate(inputs, max_length=50, num_return_sequences=1)
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
