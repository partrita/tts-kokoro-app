# tts-kokoro-app

local app for Kokoro TTS.

## What is that?

[Kokoro](https://huggingface.co/hexgrad/Kokoro-82M) is an open-weight TTS model with 82 million parameters. Despite its lightweight architecture, it delivers comparable quality to larger models while being significantly faster and more cost-efficient. With Apache-licensed weights, Kokoro can be deployed anywhere from production environments to personal projects.

## Web Application Usage

This project provides a web application interface for Text-to-Speech (TTS) generation using the Kokoro model. The application allows you to easily convert text content into audible speech directly in your browser.

## Setup Instructions

1.  Prerequisites:
    *   `uv`: A fast Python package manager and resolver. [Install uv](https://github.com/astral-sh/uv).
    *   `ffmpeg`: Must be installed on your system for audio processing (MP3 export).
        *   On macOS: `brew install ffmpeg`
        *   On Debian/Ubuntu: `sudo apt-get install ffmpeg`
        *   On other systems: Use your respective package manager.

2.  Clone the Repository:
    ```bash
    gh repo clone partrita/tts-kokoro-app
    cd tts-kokoro-app
    ```

3.  Sync Dependencies (Automatic Venv Creation):
    ```bash
    uv sync
    ```

**Important Note on Disk Space**: The `kokoro` TTS library has dependencies (like PyTorch) that can be very large. Ensure you have sufficient disk space available (several GB).

## Running the Application

1.  Start the Flask Web Server using uv:
    ```bash
    uv run python -m app.main
    ```
2.  The server will typically start and be accessible at `http://127.0.0.1:5001/` or `http://0.0.0.0:5001/`. Check the output in your terminal for the exact address.

## Using the Application

1.  Open your web browser and navigate to the address shown when you started the server (e.g., `http://127.0.0.1:5001/`).
2.  The text content from the file `data/LLM_engineer.txt` will be displayed on the page.
3.  Click the "Generate Audio" button. This will trigger the TTS conversion process for the displayed text.
4.  Once the audio is generated, it can be played using the audio player element that appears on the page. The status message will indicate when generation is complete.

## Legacy Command-Line Usage

While the primary interface is now the web application, the underlying TTS engine can still be accessed via the command line for specific use cases.

### Install dependency (if not done for web app)

Ensure you have cloned the repository and have `ffmpeg` installed as described in the "Setup Instructions" section. If you haven't set up for the web application, you might use `uv` (if preferred, though `pip` with `requirements.txt` is now standard for this project):
```bash
# Example using uv, if you have it and prefer it for managing this specific script's environment
# uv sync
# Otherwise, ensure your environment from the web app setup is active.
```

### Run python script

The `app/run.py` script can be used to generate audio directly:
```bash
python app/run.py -n welcome -i data/welcome.txt -o data/
```
This command will:
- Take text from `data/welcome.txt`.
- Generate an audio file named `welcome.mp3`.
- Save it in the `data/` directory.

The `generate_audio` function within `app/run.py` is now configured to save audio into the `static/` directory when called by the web application. If using `app/run.py` directly as a script, its `main()` function still uses the command-line arguments for output paths.

