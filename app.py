from flask import Flask, request, jsonify

app = Flask(__name__)
LIBRARY_DB = {}  # In-memory database

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# v1: Add Books
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    book_id, title, author = data.get("id"), data.get("title"), data.get("author")
    if not book_id or not title or not author:
        return jsonify({"error": "Missing parameters"}), 400
    LIBRARY_DB[book_id] = {"title": title, "author": author, "issued_to": None}
    return jsonify({"message": f"Book '{title}' added (v1)."}), 201

# v2: Issue Book
@app.route('/books/issue', methods=['POST'])
def issue_book():
    data = request.json
    book_id, student_id = data.get("id"), data.get("student_id")
    if book_id not in LIBRARY_DB:
        return jsonify({"error": "Book not found"}), 404
    LIBRARY_DB[book_id]["issued_to"] = student_id
    return jsonify({"message": f"Book issued to {student_id} (v2)."}), 200

# v3: Return Book
@app.route('/books/return', methods=['POST'])
def return_book():
    data = request.json
    book_id = data.get("id")
    if book_id not in LIBRARY_DB:
        return jsonify({"error": "Book not found"}), 404
    LIBRARY_DB[book_id]["issued_to"] = None
    return jsonify({"message": "Book marked as returned (v3)."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
