from .models import Course
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Initialize GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

def summarize_course(course_id):
    """
    Summarize a course based on its topics and materials using GPT-2.
    """
    try:
        course = Course.objects.get(id=course_id)
        
        # Combine course topics and materials to form a summary prompt
        content = f"Course: {course.title}\nDescription: {course.description}\nTopics: {', '.join(course.topics)}\nMaterials: {course.materials}"
        
        # Encode content for GPT-2
        inputs = tokenizer.encode(content, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(inputs, max_length=250, num_return_sequences=1, no_repeat_ngram_size=2, early_stopping=True)
        
        # Decode and return the summary
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    
    except Course.DoesNotExist:
        return "Course not found."
