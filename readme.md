# Tales That Talk 🔊

**Tales That Talk** is a web application that helps children practice stories and expand vocabulary in any language. Kids follow along as a narrator reads each page, encouraging them to repeat aloud and practice spoken language skills. The app enables immersive learning by combining interactive stories with custom text and images, fostering engagement and language development in a playful, educational setting.

## Features

- Create new stories with configurable age, difficulty, and language.
- Narrate each page using TTS (Text-to-Speech) for a read-aloud experience.
- Generate story with LLM and images for each page.
- Customize each page by uploading images or modifying text.

## Project Structure

- **app.py**: Main Flask application with routes for creating, editing, and saving stories.
- **language_model_utils.py**: Generates story text using language models.
- **templates/**: HTML templates for various views, including the main library and the "Add Story" interface.
- **static/**: Static files like CSS and images.
- **books/**: Directory where saved stories are stored in a structured format.

## Getting Started

1. **Install Requirements**:
    ```bash
    pip install -r requirements.txt
    ```

2. **Add OpenAI API Key**:
   - Create a `.env` file in the root directory of your project.
   - Add your OpenAI API key to the `.env` file in the following format:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     ```

3. **Run the App**:
    ```bash
    python app.py
    ```

4. **Access**:
   Visit `http://127.0.0.1:5000` to access the application.

## Customization

- **Testing with Low-Cost Models**:
   - By default, the application uses `gpt-4o-mini` and `dall-e-2` for low-cost testing. 
   - For improved results, you can change these to `gpt-4o` and `dall-e-3` in `language_model_utils.py`.

- **Alternative Models**:
   - You can also use other models like **LLaMA 3.2 (1B)** by referring to the file `language_model_utils - LLaMA 3.2.py`.
   - To switch to LLaMA models, install the dependencies listed in `requirements - LLaMA 3.2.txt` to ensure compatibility.
