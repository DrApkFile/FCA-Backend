import PyPDF2
from io import BytesIO
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from .models import UploadedFile

# Initialize GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

def summarize_pdf(file_instance_id):
    """
    Extract text from the PDF file and summarize it using GPT-2.
    """
    # Fetch the file instance from the database
    uploaded_file = UploadedFile.objects.get(id=file_instance_id)
    
    with open(uploaded_file.file.path, 'rb') as file:
        # Read the PDF file
        reader = PyPDF2.PdfFileReader(file)
        text = ""
        
        # Extract text from each page
        for page_num in range(reader.getNumPages()):
            page = reader.getPage(page_num)
            text += page.extract_text()
    
    # Generate summary using GPT-2 (with a max length to prevent too long generations)
    inputs = tokenizer.encode(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=200, num_return_sequences=1, no_repeat_ngram_size=2, early_stopping=True)
    
    # Decode the generated summary and return
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
