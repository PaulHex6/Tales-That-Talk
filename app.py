from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import os

app = Flask(__name__)

@app.route('/books/<path:filename>')
def book_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'books'), filename)

# Load book metadata for the main screen
def load_books():
    books = []
    for folder in os.listdir("books"):
        book_path = os.path.join("books", folder, "book.json")
        if os.path.isfile(book_path):
            try:
                with open(book_path, "r") as f:
                    book_data = json.load(f)
                    books.append({
                        "title": book_data.get("title", "Unknown Title"),
                        "genre": book_data.get("genre", "Unknown Genre"),
                        "difficulty": book_data.get("difficulty", "Unknown Difficulty"),
                        "age": book_data.get("age", "Unknown Age"),
                        "language": book_data.get("language", "en-US"),  # Default to en-US if not specified
                        "cover": f"/books/{folder}/{book_data.get('cover', '')}",
                        "folder": folder
                    })
            except json.JSONDecodeError:
                print(f"Error decoding JSON for {folder}")
    return books

@app.route("/")
def index():
    books = load_books()
    return render_template("index.html", books=books)

@app.route("/story/<folder>")
def story(folder):
    book_path = os.path.join("books", folder, "book.json")
    if os.path.isfile(book_path):
        try:
            with open(book_path, "r") as f:
                book_data = json.load(f)
            return render_template("story.html", book_data=book_data, folder=folder)
        except json.JSONDecodeError:
            return "Error decoding book data", 500
    return "Story not found", 404

@app.route("/get_story/<folder>")
def get_story(folder):
    book_path = os.path.join("books", folder, "book.json")
    if os.path.isfile(book_path):
        try:
            with open(book_path, "r") as f:
                book_data = json.load(f)
            return jsonify(book_data)
        except json.JSONDecodeError:
            return jsonify({"error": "Error decoding book data"}), 500
    return jsonify({"error": "Story not found"}), 404

if __name__ == "__main__":
    app.run()
