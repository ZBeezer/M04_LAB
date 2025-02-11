from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# Book storage
books = []


# Create a new Book
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required."}), 400

    # Required fields
    required_fields = ['id', 'book_name', 'author', 'publisher']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing one or more required fields: id, book_name, author, publisher."}), 400

    # Check for duplicate book ids
    if any(book['id'] == data['id'] for book in books):
        return jsonify({"error": "Book id already exists."}), 400

    books.append(data)
    return jsonify(data), 201


# Retrieve all Books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books), 200


# Retrieve a specific Book by id
@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    for book in books:
        if book['id'] == book_id:
            return jsonify(book), 200
    return jsonify({"error": "Book not found."}), 404


# Update a Book by id
@app.route('/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required."}), 400

    for book in books:
        if book['id'] == book_id:
            # Update the provided fields
            book['book_name'] = data.get('book_name', book['book_name'])
            book['author'] = data.get('author', book['author'])
            book['publisher'] = data.get('publisher', book['publisher'])
            return jsonify(book), 200

    return jsonify({"error": "Book not found."}), 404


# Delete a Book by id
@app.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    for index, book in enumerate(books):
        if book['id'] == book_id:
            removed_book = books.pop(index)
            return jsonify({
                "message": "Book deleted.",
                "book": removed_book
            }), 200

    return jsonify({"error": "Book not found."}), 404


if __name__ == '__main__':
    app.run(debug=True)
