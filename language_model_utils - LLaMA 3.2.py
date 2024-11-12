# Alternative LLM using LLaMA 3.2 - rename this file to language_model_utils and pip install -r 'requirements - LLaMA 3.2.txt'

from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the tokenizer and model once when the module is imported
tokenizer = AutoTokenizer.from_pretrained("alpindale/Llama-3.2-1B")
model = AutoModelForCausalLM.from_pretrained("alpindale/Llama-3.2-1B")

def generate_llm_text(prompt, max_new_tokens=50):
    """
    General function to generate text using the LLM model.
    """
    print("LLaMA is thinking, please wait...")
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)

    # Generate text
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,        # Sets maximum number of tokens to generate (up to 50 here)
        temperature=0.7,                      # Controls randomness; lower values make output more deterministic
        num_beams=3,                          # Uses beam search with 3 beams for more precise, focused output
        repetition_penalty=5.0,               # Discourages repetition; higher values reduce repeated phrases
        eos_token_id=tokenizer.eos_token_id,  # Sets an end-of-sequence token to stop generation after a response
        num_return_sequences=1,               # Generates multiple outputs; set to 3 to get three variations of response
        do_sample=True                        # Enables sampling-based generation (needed if using temperature)

        # Alternative parameters that can be used instead:
        # top_k=50,                           # Limits sampling to top-k most probable tokens (useful for focused sampling)
        # top_p=0.9,                          # Uses nucleus (top-p) sampling, considering tokens with cumulative probability p
        # length_penalty=0.3                  # Adjusts preference for shorter or longer responses; >1 favors longer responses
    )

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"LLaMA reply: {generated_text}")
    return generated_text

def generate_page_text(prompt):
    """
    Specific function for generating text for a single page.
    """
    refined_prompt = f"Write a short, engaging story for a 5-year-old about '{prompt}'. Keep it under 30 words."
    generated_text = generate_llm_text(refined_prompt, max_new_tokens=50)
    if refined_prompt in generated_text:
        generated_text = generated_text.replace(refined_prompt, "").strip()
    return generated_text

def generate_full_story(title, genre, age, difficulty, language, prompt):
    """
    Function to generate a full story based on the provided parameters.
    """
    refined_prompt = (
        f"Write a children's story titled '{title}' in {language}, suitable for ages {age}, "
        f"with a {difficulty} difficulty level. The genre is {genre}. "
        f"The story should be about {prompt}. Limit the story to 20 sentences."
    )
    generated_text = generate_llm_text(refined_prompt, max_new_tokens=500)
    if refined_prompt in generated_text:
        generated_text = generated_text.replace(refined_prompt, "").strip()
    return generated_text
