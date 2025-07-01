import os
from flask import Flask, render_template, jsonify, request
from .run import process_text_file, generate_audio

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Define the path to the data directory relative to this script (app/main.py)
# ../data will go up one level from 'app' to the project root, then into 'data'
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
TEXT_FILE_PATH = os.path.join(DATA_DIR, "LLM_engineer.txt")

@app.route('/', methods=['GET'])
def index():
    """
    Renders the main page with text content.
    """
    try:
        file_content = process_text_file(TEXT_FILE_PATH)
    except FileNotFoundError:
        # Fallback or error handling if the primary file is not found
        # For now, let's provide a default text and log an error or message
        print(f"Error: Text file not found at {TEXT_FILE_PATH}. Using default text.")
        file_content = "The specified text file was not found. Please check the path."
    return render_template('index.html', text_content=file_content)

@app.route('/generate-audio', methods=['POST'])
def trigger_audio_generation():
    """
    Generates audio from the text file and returns the path to the audio file.
    """
    try:
        text_content = process_text_file(TEXT_FILE_PATH)
        # The output filename "llm_guide_audio" will have ".mp3" appended by generate_audio
        # and will be saved in the "static" directory.
        audio_file_path = generate_audio(text_content, "llm_guide_audio")
        return jsonify({"audio_path": audio_file_path})
    except FileNotFoundError:
        return jsonify({"error": f"Text file not found at {TEXT_FILE_PATH}"}), 404
    except Exception as e:
        # Log the exception for debugging
        print(f"Error during audio generation: {e}")
        return jsonify({"error": "Failed to generate audio"}), 500

if __name__ == '__main__':
    # Make sure the static directory exists, as generate_audio might need it
    static_dir_path = os.path.join(os.path.dirname(__file__), "..", "static")
    if not os.path.exists(static_dir_path):
        os.makedirs(static_dir_path)
        print(f"Created static directory at {static_dir_path}")

    app.run(debug=True, host='0.0.0.0', port=5001)
