from django.http import JsonResponse
from .kronos import KronosLLM
from django.views.decorators.csrf import csrf_exempt
import json

# Instantiate the Kronos LLM
kronos = KronosLLM()

@csrf_exempt
def generate_response(request):
    """
    API endpoint to generate a response from the GPT-2 model based on user input.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_input = data.get('user_input', '')

            if not user_input:
                return JsonResponse({'error': 'No input text provided.'}, status=400)

            response = kronos.generate_response(user_input)
            return JsonResponse({'response': response}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method. POST required.'}, status=400)

@csrf_exempt
def summarize_text(request):
    """
    API endpoint to summarize a given text using the GPT-2 model.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text_to_summarize = data.get('text', '')

            if not text_to_summarize:
                return JsonResponse({'error': 'No text provided for summarization.'}, status=400)

            summary = kronos.summarize_text(text_to_summarize)
            return JsonResponse({'summary': summary}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method. POST required.'}, status=400)

@csrf_exempt
def fine_tune(request):
    """
    API endpoint to trigger fine-tuning of the model with new data.
    """
    if request.method == 'POST':
        try:
            # Trigger the fine-tuning process
            from .fine_tune import fine_tune_model
            fine_tune_model()  # You can customize this to run asynchronously
            return JsonResponse({'status': 'Fine-tuning process started.'}, status=200)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method. POST required.'}, status=400)
