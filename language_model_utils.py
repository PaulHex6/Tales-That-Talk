# language_model_utils.py
import openai
import os
import requests
import uuid
from flask import url_for
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

# Initialize OpenAI client
load_dotenv()
client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def generate_llm_text(prompt, max_new_tokens=50):
    """
    General function to generate text using the GPT-4o model.
    """
    print(f"GPT-4o is generating reply to '{prompt}', please wait...")
    
    # Generate text
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a creative assistant and storyteller specializing in writing engaging and age-appropriate content for books."},
            {"role": "user", "content": prompt}
        ]
    )

    generated_text = chat_completion.choices[0].message.content.strip()
    print(f"GPT-4o reply: {generated_text}")
    return generated_text

def generate_page_text(title, genre, age, difficulty, language, prompt, previous_text='', next_text=''):
    """
    Generates text for a page based on the provided prompt and additional context.
    """
    # Refine the prompt to incorporate additional context
    refined_prompt = (
        f"Write 1-2 sentences for one page of an engaging story titled '{title}' in {language}, "
        f"targeted at ages {age} with a {difficulty} difficulty level. "
        f"The genre is {genre}. Use the following story prompt: '{prompt}'.\n"
    )

    # Add context from previous and next text if available
    if previous_text:
        refined_prompt += f"Consider that the previous text on the story page was: '{previous_text}'.\n"
    if next_text:
        refined_prompt += f"Plan for continuity, as the next page might start with: '{next_text}'.\n"

    # Generate the text using the refined prompt
    generated_text = generate_llm_text(refined_prompt, max_new_tokens=50)
    return generated_text


def generate_full_story(title, genre, age, difficulty, language, prompt):
    """
    Function to generate a full story based on the provided parameters.
    """
    refined_prompt = (
        f"Write a children's story titled '{title}' in {language}, suitable for ages {age}, "
        f"with a {difficulty} difficulty level. The genre is {genre}. "
        f"The story should be about '{prompt}'. Story should be 10 to 20 sentences."
    )
    generated_text = generate_llm_text(refined_prompt, max_new_tokens=500)
    return generated_text

def generate_image(prompt):
    print(f"Dalle is generating image '{prompt}', please wait...")
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        n=1,
        size="512x512"          #minimum 1024x1024 for dall-e-3
    )
    image_url = response.data[0].url

    # Download the image
    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        # Convert to .webp format
        unique_filename = f"{uuid.uuid4()}.webp"
        filepath = os.path.join('static', 'temp_images', unique_filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Open the image and save it in .webp format
        image = Image.open(BytesIO(image_response.content))
        image.save(filepath, "WEBP")
        print(f"Path: {filepath}\{unique_filename}")

        # Return the URL to the image and filename
        return {
            'image_url': url_for('static', filename=f'temp_images/{unique_filename}'),
            'filename': os.path.join('temp_images', unique_filename)  # Relative path from 'static' folder
        }
    else:
        raise Exception('Failed to download image')
