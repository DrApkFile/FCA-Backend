import pandas as pd
from transformers import GPT2Tokenizer, TFGPT2LMHeadModel
from tensorflow.keras.optimizers import Adam
import tensorflow as tf

def fine_tune_model(data_path='training.csv', model_save_path='chatbot/ai/fine_tuned_model'):
    """
    Fine-tune the GPT-2 model with the data from the training.csv file.
    """
    # Load dataset
    data = pd.read_csv(data_path)
    summaries = data['summary'].tolist()
    documents = data['document'].tolist()

    # Load pre-trained GPT-2 model and tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = TFGPT2LMHeadModel.from_pretrained('gpt2')

    # Tokenize inputs and labels
    input_ids = tokenizer(documents, return_tensors='tf', padding=True, truncation=True).input_ids
    labels = tokenizer(summaries, return_tensors='tf', padding=True, truncation=True).input_ids

    # Compile the model with Adam optimizer
    model.compile(optimizer=Adam(learning_rate=5e-5), loss=model.compute_loss)

    # Fine-tune the model
    model.fit(input_ids, labels, epochs=3, batch_size=2)  # Adjust batch_size if needed

    # Save the fine-tuned model
    model.save_pretrained(model_save_path)
    tokenizer.save_pretrained(model_save_path)

    print(f"Model fine-tuned and saved at {model_save_path}")

# Fine-tune the model using the data
fine_tune_model()
