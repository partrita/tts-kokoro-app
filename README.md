# tts-kokoro-app

local app for Kokoro TTS.

## How to use

### Install dependency

clone the repo and use `uv` to installation.

```bash
gh repo clone partrita/tts-kokoro-app
cd tts-kokoro-app
uv sync
```

### Run python script 

```bash
uv run app/run.py -n welcome -i data/welcome.txt -o data/
```
