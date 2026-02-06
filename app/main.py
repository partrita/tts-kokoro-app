import os
from flask import Flask, render_template, jsonify, request
from .run import process_text_file, generate_audio

# Use absolute paths for templates and static
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

DATA_DIR = os.path.join(base_dir, "data")
DEFAULT_TEXT_FILE = os.path.join(DATA_DIR, "LLM_engineer.txt")

@app.route('/', methods=['GET'])
def index():
    """Renders the main page."""
    try:
        default_content = ""
        if os.path.exists(DEFAULT_TEXT_FILE):
            default_content = process_text_file(DEFAULT_TEXT_FILE)
    except Exception as e:
        print(f"Error reading default file: {e}")
        default_content = "Welcome! Type your text here to generate speech."
    
    return render_template('index.html', text_content=default_content)

@app.route('/generate-audio', methods=['POST'])
def trigger_audio_generation():
    """Generates audio from text (either default or user-provided)."""
    try:
        data = request.get_json() or {}
        text_content = data.get('text')
        voice = data.get('voice', 'af_heart')
        speed = float(data.get('speed', 1.0))

        if not text_content:
            if os.path.exists(DEFAULT_TEXT_FILE):
                text_content = process_text_file(DEFAULT_TEXT_FILE)
            else:
                return jsonify({"error": "No text provided and default file missing."}), 400

        # Create a unique filename if needed, or stick to a fixed one for simplicity
        audio_file_path = generate_audio(text_content, "tts_output", voice=voice, speed=speed)
        return jsonify({"audio_path": audio_file_path})
    except Exception as e:
        print(f"Error during audio generation: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
    app.run(debug=True, host='0.0.0.0', port=5001)
