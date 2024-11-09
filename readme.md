# Tales That Talk

📖 **Tales That Talk** is a web application that helps children practice stories and expand vocabulary in any language. Kids follow along as a narrator reads each page, encouraging them to repeat aloud and practice spoken language skills. The app enables immersive learning by combining interactive stories with custom text and images, fostering engagement and language development in a playful, educational setting.

## Features

- Create new stories with configurable age, difficulty, and language.
- Generate text and images for each page with AI assistance.
- Customize each page by uploading images or modifying text.

## Project Structure

- **app.py**: Main Flask application with routes for creating, editing, and saving stories.
- **templates/**: HTML templates for various views, including the main library and the "Add Story" interface.
- **static/**: Static files like CSS and images.
- **books/**: Directory where saved stories are stored in a structured format.

## Getting Started

1. **Install Requirements**:
    ```bash
    pip install -r requirements.txt
    ```

2. **Run the App**:
    ```bash
    python app.py
    ```

3. **Access**:
   Visit `http://127.0.0.1:5000` to access the application.

