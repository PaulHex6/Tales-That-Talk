from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import json
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'books'

@app.route('/books/<path:filename>')
def book_static(filename):
    return send_from_directory(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), filename)

def load_books():
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

@app.route("/")
def index():
    books = load_books()
    return render_template("index.html", books=books)

from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify

@app.route("/story/<folder>")
def story(folder):
    book_path = os.path.join(app.config['UPLOAD_FOLDER'], folder, 'book.json')
    if os.path.isfile(book_path):
        with open(book_path, "r", encoding="utf-8") as f:
            book_data = json.load(f)

        # Serialize book_data to JSON to prevent special character issues
        book_data_json = json.dumps(book_data, ensure_ascii=False)
        return render_template("story.html", book_data=book_data_json, folder=folder)

    return "Story not found", 404

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

        # Clean the title for use in folder naming (optional but recommended to remove spaces or special characters)
        folder_name = title.replace(" ", "_").replace("/", "_")

        # Prepare pages data
        pages = []
        page_texts = request.form.getlist('page_text')
        page_images = request.files.getlist('page_image')

        for idx, text in enumerate(page_texts):
            image_file = page_images[idx] if idx < len(page_images) else None
            image_filename = ""
            if image_file and image_file.filename != '':
                image_filename = f"page_{idx+1}_{image_file.filename}"
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name, image_filename)
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                image_file.save(image_path)
            pages.append({"text": text.strip(), "image": image_filename})

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

        # Create the book directory using the title and save the JSON file
        book_folder = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
        os.makedirs(book_folder, exist_ok=True)
        book_json_path = os.path.join(book_folder, 'book.json')
        with open(book_json_path, 'w', encoding='utf-8') as f:
            json.dump(book_data, f, indent=2, ensure_ascii=False)

        return redirect(url_for('story', folder=folder_name))

    # Render the add story form
    return render_template("add_story.html")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
