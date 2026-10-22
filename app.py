from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock database mapping book IDs to records
# Format: book_id: {"title": str, "author": str, "issued_to": str/None}
LIBRARY_DB = {}

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# ==========================================
# VERSION 1 FEATURE: Add Books
# ==========================================
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    book_id = data.get("id")
    title = data.get("title")
    author = data.get("author")
    
    if not book_id or not title or not author:
        return jsonify({"error": "Missing parameters"}), 400
        
    if book_id in LIBRARY_DB:
        return jsonify({"error": "Book already exists"}), 400
        
    LIBRARY_DB[book_id] = {
        "title": title,
        "author": author,
        "issued_to": None
    }
    return jsonify({"message": f"Book '{title}' successfully added."}), 201

# ==========================================
# VERSION 2 FEATURE: Issue Book
# ==========================================
@app.route('/books/issue', methods=['POST'])
def issue_book():
    data = request.json
    book_id = data.get("id")
    student_id = data.get("student_id")
    
    if book_id not in LIBRARY_DB:
        return jsonify({"error": "Book not found"}), 404
        
    if LIBRARY_DB[book_id]["issued_to"] is not None:
        return jsonify({"error": "Book is already issued"}), 400
        
    LIBRARY_DB[book_id]["issued_to"] = student_id
    return jsonify({"message": f"Book allocated to student {student_id}."}), 200

# ==========================================
# VERSION 3 FEATURE: Return Book
# ==========================================
@app.route('/books/return', methods=['POST'])
def return_book():
    data = request.json
    book_id = data.get("id")
    
    if book_id not in LIBRARY_DB:
        return jsonify({"error": "Book not found"}), 404
        
    if LIBRARY_DB[book_id]["issued_to"] is None:
        return jsonify({"error": "Book was not issued"}), 400
        
    LIBRARY_DB[book_id]["issued_to"] = None
    return jsonify({"message": "Book marked as returned and available."}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
