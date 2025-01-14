from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Replace with your Google API key
GOOGLE_API_KEY = "AIzaSyApLgeFUZllA7xlSYWvHD-z92AoTOfyXY0"
GOOGLE_TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"

@app.route('/')
def index():
    """
    Serve the main HTML page.
    """
    return render_template('index.html')


@app.route('/translate', methods=['POST'])
def translate_text():
    """
    Handle text translation requests using Google Translate API.
    """
    # Parse JSON input
    data = request.json
    source_text = data.get('text')
    target_language = data.get('target_language', 'en')  # Default to English

    # Validate input
    if not source_text:
        return jsonify({"error": "Text to translate is required"}), 400

    # Google Translate API request
    payload = {
        "q": source_text,
        "target": target_language,
        "key": GOOGLE_API_KEY
    }
    response = requests.post(GOOGLE_TRANSLATE_URL, json=payload)

    # Handle API response
    if response.status_code != 200:
        return jsonify({"error": "Failed to translate text", "details": response.text}), response.status_code

    # Extract translation
    translated_text = response.json().get('data', {}).get('translations', [])[0].get('translatedText', "Error: No translation found.")

    return jsonify({"translated_text": translated_text})


if __name__ == '__main__':
    app.run(debug=True)
