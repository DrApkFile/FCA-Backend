from youtube_transcript_api import YouTubeTranscriptApi
from .models import YouTubeLink
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Initialize GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

def summarize_youtube_video(youtube_url):
    """
    Given a YouTube URL, fetch the transcript and summarize it using GPT-2.
    """
    # Extract video ID from URL
    video_id = extract_video_id(youtube_url)
    
    if video_id:
        try:
            # Fetch the transcript of the YouTube video
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = " ".join([entry['text'] for entry in transcript])
            
            # Summarize the transcript using GPT-2
            summary = summarize_text(transcript_text)
            
            # Store the link and transcript in the database
            link_instance = YouTubeLink.objects.create(url=youtube_url, transcript=transcript_text)
            
            return summary
        
        except Exception as e:
            return f"Error fetching transcript: {str(e)}"
    
    return "Invalid YouTube URL or video ID not found."

def extract_video_id(url):
    """
    Extracts YouTube video ID from the given URL.
    """
    import re
    match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    return None

def summarize_text(text):
    """
    Summarize the provided text using GPT-2.
    """
    inputs = tokenizer.encode(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=200, num_return_sequences=1, no_repeat_ngram_size=2, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
