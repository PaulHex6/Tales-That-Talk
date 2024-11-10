# llama_api.py
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the tokenizer and model once when the module is imported
tokenizer = AutoTokenizer.from_pretrained("alpindale/Llama-3.2-1B")
model = AutoModelForCausalLM.from_pretrained("alpindale/Llama-3.2-1B")

def generate_text(prompt, max_new_tokens=50):
    # Tokenize the input prompt
    refined_prompt = f"Write a short, engaging story for a 5-year-old about '{prompt}'. Keep it under 30 words."
    print(refined_prompt, flush=True)

    inputs = tokenizer(refined_prompt, return_tensors="pt", truncation=True, max_length=512)

    # Generate text
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens, num_return_sequences=1)

    # Decode the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Remove the prompt part from the generated text
    if refined_prompt in generated_text:
        generated_text = generated_text.replace(refined_prompt, "").strip()

    return generated_text
