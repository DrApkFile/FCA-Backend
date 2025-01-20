from transformers import GPT2Tokenizer, TFGPT2LMHeadModel
import tensorflow as tf

class KronosLLM:
    def __init__(self, model_path='data/model/kronos_model', save_model_path='data/kronos_model'):
        """
        Initialize the Kronos LLM with a pre-trained model or a fine-tuned model.
        Optionally save the model to the specified path after usage.
        """
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        self.model = TFGPT2LMHeadModel.from_pretrained(model_path)
        self.save_model_path = save_model_path  # Location to save the model after use or fine-tuning

    def generate_response(self, input_text):
        """
        Generate a response from the model based on the provided input.
        """
        inputs = self.tokenizer.encode(input_text, return_tensors='tf')
        outputs = self.model.generate(inputs, max_length=100, num_return_sequences=1)

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    def summarize_text(self, input_text):
        """
        Generate a summary of the provided text by limiting the length.
        """
        inputs = self.tokenizer.encode(input_text, return_tensors='tf')
        summary = self.model.generate(inputs, max_length=150, num_return_sequences=1)

        return self.tokenizer.decode(summary[0], skip_special_tokens=True)

    def save_model(self):
        """
        Save the fine-tuned model to the specified path (e.g., `data/kronos_model`).
        """
        self.model.save_pretrained(self.save_model_path)
        self.tokenizer.save_pretrained(self.save_model_path)
        print(f"Model saved to {self.save_model_path}")
