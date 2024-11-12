import openai
import os
from dotenv import load_dotenv

# Initialize OpenAI client
load_dotenv()
client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def generate_llm_text(prompt, max_new_tokens=50):
    """
    General function to generate text using the GPT-4o model.
    """
    print("GPT-4o is thinking, please wait...")
    
    # Generate text
    chat_completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    generated_text = chat_completion.choices[0].message.content.strip()
    print(f"GPT-4o reply: {generated_text}")
    return generated_text

def generate_page_text(prompt):
    """
    Specific function for generating text for a single page.
    """
    refined_prompt = f"Write a short, engaging story for a 5-year-old about '{prompt}'. Keep it under 30 words."
    generated_text = generate_llm_text(refined_prompt, max_new_tokens=50)
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
    return generated_text
