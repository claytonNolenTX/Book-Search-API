    """This is the logic (backend) to the web application that gets information from the open api.
    
    Author: Clayton Nolen
    Last Modified: 18 November 2024
    """

from flask import Flask, request, jsonify, send_from_directory
import os
import requests
from flask_cors import CORS

# Initialize Flask application
app = Flask(__name__, static_folder=os.path.join(os.getcwd(), '..', 'frontend'), static_url_path='/')

# Enable Cross-Origin Resource Sharing (CORS) for all routes
CORS(app)

@app.route('/search', methods=['GET'])
def search_books():
    """Search for books using the OpenLibrary API based on query parameters: title, author, or subject.

    This endpoint accepts three optional query parameters:
    - title (str): Search query for the book title.
    - author (str): Search query for the author's name.
    - subject (str): Search query for the book's subject.

    If any of these parameters are provided, a search request is sent to the OpenLibrary API. 
    The response is processed, and a list of books is returned with the following fields:
    - title: The title of the book.
    - author: A comma-separated list of authors.
    - link: URL to the OpenLibrary page of the book.
    - image: URL of the book cover image (if available).

    If no query parameters are provided, or if an error occurs, an error message is returned.

    Returns:
        JSON: A list of books matching the search query or an error message if no query is provided or an error occurs.

    Error responses:
        - 400: If no valid query parameters (title, author, or subject) are provided.
        - 500: If there is an error when calling the OpenLibrary API.
    """
    # Retrieve query parameters
    query = request.args.get('title', '').strip()
    author = request.args.get('author', '').strip()
    subject = request.args.get('subject', '').strip()

    # Build the search query string
    search_params = []
    if query:
        search_params.append(f'title={query}')
    if author:
        search_params.append(f'author={author}')
    if subject:
        search_params.append(f'subject={subject}')

    # Return an error if no query parameter is provided
    if not search_params:
        return jsonify({'error': 'At least one of title, author, or subject query parameters is required'}), 400

    # Join the parameters with '&' and call the OpenLibrary API
    search_query = '&'.join(search_params)

    try:
        response = requests.get(f'https://openlibrary.org/search.json?{search_query}')
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Process the response data
        data = response.json()
        books = []

        for doc in data.get('docs', []):
            book = {
                'title': doc.get('title', 'N/A'),
                'author': ', '.join(doc.get('author_name', ['N/A'])),
                'link': f"https://openlibrary.org{doc.get('key', '')}",
                'image': f"http://covers.openlibrary.org/b/id/{doc.get('cover_i')}-S.jpg" if 'cover_i' in doc else None
            }
            books.append(book)

        return jsonify(books)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


@app.route('/')
def index():
    """Serve the frontend HTML file (index.html).

    This route serves the `index.html` file from the 'frontend' directory when a user accesses the root URL.

    Returns:
        Response: The `index.html` file located in the 'frontend' directory.
    """
    # Debugging: print the path Flask is using to locate index.html
    print(f"Serving index.html from: {os.path.join(os.getcwd(), '..', 'frontend')}")
    return send_from_directory(os.path.join(os.getcwd(), '..', 'frontend'), 'index.html')


if __name__ == '__main__':
    """Starts the Flask application server on port 5001.

    Starts a development server for Flask, which provides the book search functionality on port 5001 (frontend).
    Note that the web app is running in debug mode.
    """
    app.run(debug=True, port=5001)
