from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Initialize GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

def answer_general_knowledge_question(question):
    """
    Answer a general knowledge question using GPT-2.
    """
    context = """
    The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France.
    It was named after the engineer Gustave Eiffel, whose company designed and built the tower.
    The Eiffel Tower was constructed between 1887 and 1889 for the 1889 World's Fair.
    It was initially criticized by some of Paris' leading artists and intellectuals for its design,
    but it has become a global cultural icon of France and one of the most recognizable structures in the world.
    """
    
    # Combine the question and context
    input_text = f"Context: {context}\nQuestion: {question}\nAnswer:"
    
    # Encode the question and context for GPT-2
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=1024, truncation=True)
    answer_ids = model.generate(inputs, max_length=200, num_return_sequences=1, no_repeat_ngram_size=2, early_stopping=True)
    
    # Decode and return the answer
    answer = tokenizer.decode(answer_ids[0], skip_special_tokens=True)
    return answer
