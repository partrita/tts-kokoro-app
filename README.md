# tts-kokoro-app

local app for Kokoro TTS.

## What is that?

[Kokoro](https://huggingface.co/hexgrad/Kokoro-82M) is an open-weight TTS model with 82 million parameters. Despite its lightweight architecture, it delivers comparable quality to larger models while being significantly faster and more cost-efficient. With Apache-licensed weights, Kokoro can be deployed anywhere from production environments to personal projects.

## How to use it.

### Install dependency

clone the repo and use `uv` and `brew` to installation.

```bash
gh repo clone partrita/tts-kokoro-app
cd tts-kokoro-app
uv sync
brew install ffmpeg # for mp3 file
```

### Run python script

```bash
uv run app/run.py -n welcome -i data/welcome.txt -o data/
```

### Make text files

[docling](https://github.com/DS4SD/docling) simplifies document processing, parsing diverse formats — including advanced PDF understanding — and providing seamless integrations with the gen AI ecosystem.
