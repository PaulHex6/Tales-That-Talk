# app.py
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import json
import os
from language_model_utils import generate_page_text, generate_full_story, generate_image
import shutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'books'
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024  # 25 MB limit

@app.route('/books/<path:filename>')
def book_static(filename):
    return send_from_directory(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), filename)

def load_books():
    #print("Loading books...")
    books = []
    for folder in os.listdir(app.config['UPLOAD_FOLDER']):
        book_path = os.path.join(app.config['UPLOAD_FOLDER'], folder, 'book.json')
        if os.path.isfile(book_path):
            try:
                # Open the file with UTF-8 encoding to handle special characters
                with open(book_path, "r", encoding="utf-8") as f:
                    book_data = json.load(f)
                cover_filename = book_data.get('cover', '')
                cover_path = f"/books/{folder}/{cover_filename}" if cover_filename else "/static/default_cover.png"

                #print(f"Loaded language for {folder}: {book_data.get('language', 'en-US')}")

                books.append({
                    "title": book_data.get("title", "Unknown Title"),
                    "genre": book_data.get("genre", "Unknown Genre"),
                    "difficulty": book_data.get("difficulty", "Unknown Difficulty"),
                    "age": book_data.get("age", "Unknown Age"),
                    "language": book_data.get("language", "en-US"),
                    "cover": cover_path,
                    "folder": folder
                })
            except json.JSONDecodeError:
                print(f"Error decoding JSON for {folder}")
    return books

current_theme = "theme-light"

@app.context_processor
def inject_theme():
    global current_theme
    return {"theme": current_theme}

@app.route("/")
def index():
    #print("Rendering index page...")
    books = load_books()
    return render_template("index.html", books=books)

@app.route("/story/<folder>")
def story(folder):
    book_path = os.path.join(app.config['UPLOAD_FOLDER'], folder, 'book.json')
    if os.path.isfile(book_path):
        with open(book_path, "r", encoding="utf-8") as f:
            book_data = json.load(f)
        
        # Pass `book_data` as-is, without additional serialization
        return render_template("story.html", book_data=book_data, folder=folder)
    return "Story not found", 404

BETA_FEATURE_PASSWORD = os.environ.get("BETA_FEATURE_PASSWORD", "pass")

#AI functionality in BETA testing, show popup to request the access
@app.route('/validate_popup', methods=['POST'])
def validate_popup():
    # Get password from the incoming request
    data = request.get_json()
    password = data.get("password", "")

    # Validate password
    if password == BETA_FEATURE_PASSWORD:
        return jsonify({"success": True})  # Password validated
    return jsonify({"success": False})  # Incorrect password

@app.route("/add_story", methods=['GET', 'POST'])
def add_story():
    if request.method == 'POST':
        # Process form data for actual saving
        title = request.form.get('title', '').strip()
        genre = request.form.get('genre', '').strip()
        age = request.form.get('age', '').strip()
        difficulty = request.form.get('difficulty', '').strip()
        language = request.form.get('language', '').strip()
        prompt = request.form.get('prompt', '').strip()

        # Validate input data
        errors = []
        if not title:
            errors.append("Title is required.")
        if not genre:
            errors.append("Genre is required.")
        if not age:
            errors.append("Age is required.")
        if not difficulty:
            errors.append("Difficulty is required.")
        if not language:
            errors.append("Language is required.")
        if not prompt:
            errors.append("Story description is required.")

        # Clean the title for use in folder naming
        folder_name = title.replace(" ", "_").replace("/", "_")

        # Prepare pages data
        pages = []
        page_texts = request.form.getlist('page_text')
        page_images = request.files.getlist('page_image')
        page_image_filenames = request.form.getlist('page_image_filename')  # Filenames for generated images

        for idx, text in enumerate(page_texts):
            # Handle uploaded image
            image_file = page_images[idx] if idx < len(page_images) else None
            image_filename = ""

            if image_file and image_file.filename != '':
                # Save uploaded image
                image_filename = f"page_{idx+1}_{image_file.filename}"
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name, image_filename)
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                image_file.save(image_path)
            else:
                # Handle generated image if no uploaded image exists
                image_filename_from_form = page_image_filenames[idx] if idx < len(page_image_filenames) else ''
                if image_filename_from_form:
                    temp_image_path = os.path.join('static', image_filename_from_form)
                    if os.path.exists(temp_image_path):
                        image_filename = f"page_{idx+1}_{os.path.basename(image_filename_from_form)}"
                        image_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name, image_filename)
                        os.makedirs(os.path.dirname(image_path), exist_ok=True)
                        shutil.move(temp_image_path, image_path)  # Move the file to the book folder
                    else:
                        print(f"Generated image not found: {temp_image_path}")

            pages.append({"text": text.strip(), "image": image_filename})

        # Handle form errors
        if errors:
            return render_template("add_story.html", errors=errors, form=request.form.to_dict(flat=False))

        # Save cover image
        cover_file = request.files.get('cover_image')
        cover_filename = ""
        if cover_file and cover_file.filename != '':
            cover_filename = f"cover_{cover_file.filename}"
            cover_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name, cover_filename)
            os.makedirs(os.path.dirname(cover_path), exist_ok=True)
            cover_file.save(cover_path)

        # Prepare book data and save to a JSON file
        book_data = {
            "title": title,
            "genre": genre,
            "age": age,
            "difficulty": difficulty,
            "language": language,
            "cover": cover_filename,
            "pages": pages
        }

        # Create the book directory and save the JSON file
        book_folder = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
        os.makedirs(book_folder, exist_ok=True)
        book_json_path = os.path.join(book_folder, 'book.json')
        with open(book_json_path, 'w', encoding='utf-8') as f:
            json.dump(book_data, f, indent=2, ensure_ascii=False)

        return redirect(url_for('story', folder=folder_name))

    # Render the add story form
    return render_template("add_story.html")

@app.route('/generate_text', methods=['POST'])
def generate_text_route():
    data = request.get_json()
    prompt = data.get('prompt', '')
    title = data.get('title', '')
    genre = data.get('genre', '')
    age = data.get('age', '')
    difficulty = data.get('difficulty', '')
    language = data.get('language', '')
    previous_text = data.get('previous_text', '')
    next_text = data.get('next_text', '')

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    
    try:
        # Generate text for a page using the expanded function
        generated_text = generate_page_text(
            title=title,
            genre=genre,
            age=age,
            difficulty=difficulty,
            language=language,
            prompt=prompt,
            previous_text=previous_text,
            next_text=next_text
        )
        return jsonify({'generated_text': generated_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_full_story', methods=['POST'])
def generate_full_story_route():
    data = request.get_json()
    title = data.get('title', '').strip()
    genre = data.get('genre', '').strip()
    age = data.get('age', '').strip()
    difficulty = data.get('difficulty', '').strip()
    language = data.get('language', '').strip()
    prompt = data.get('prompt', '').strip()

    # Validate input data
    errors = []
    if not title:
        errors.append("Title is required.")
    if not genre:
        errors.append("Genre is required.")
    if not age:
        errors.append("Age is required.")
    if not difficulty:
        errors.append("Difficulty is required.")
    if not language:
        errors.append("Language is required.")
    if not prompt:
        errors.append("Story description is required.")

    if errors:
        return jsonify({'error': ' '.join(errors)}), 400

    try:
        # Generate full story using LLaMA model
        generated_story = generate_full_story(title, genre, age, difficulty, language, prompt)
        return jsonify({'generated_story': generated_story})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_image', methods=['POST'])
def generate_image_route():
    data = request.get_json()
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    try:
        image_data = generate_image(prompt)
        return jsonify(image_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run("0.0.0.0", int(os.getenv("PORT", 5000)), debug=True, use_reloader=False)

