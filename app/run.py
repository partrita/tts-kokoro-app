import argparse
import os
from typing import List, Optional
from kokoro import KPipeline
import soundfile as sf
import numpy as np
from pydub import AudioSegment
import io
import warnings

# Ignore specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module="torch.nn.modules.rnn")
warnings.filterwarnings(
    "ignore", category=FutureWarning, module="torch.nn.utils.weight_norm"
)

# Global pipeline to avoid reloading models on every request
_pipeline_cache = {}

def get_pipeline(lang_code: str = "a") -> KPipeline:
    if lang_code not in _pipeline_cache:
        _pipeline_cache[lang_code] = KPipeline(lang_code=lang_code)
    return _pipeline_cache[lang_code]


def process_text_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    return text


def generate_audio(text: str, output_filename_no_ext: str, voice: str = "af_heart", speed: float = 1.0) -> str:
    pipeline = get_pipeline(lang_code="a" if voice.startswith("a") else "b")
    generator = pipeline(text, voice=voice, speed=speed, split_pattern=r"\n+")

    all_audio: List[np.ndarray] = []

    for i, (gs, ps, audio) in enumerate(generator):
        all_audio.append(audio)

    if not all_audio:
        raise ValueError("No audio segments generated.")

    # Concatenate all audio segments
    combined_audio: np.ndarray = np.concatenate(all_audio)

    # Use absolute paths to be safe
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_folder = os.path.join(base_dir, "static", "audio")
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_filename_with_ext = f"{output_filename_no_ext}.mp3"
    output_path = os.path.join(output_folder, output_filename_with_ext)

    # Save to buffer
    wav_io = io.BytesIO()
    sf.write(wav_io, combined_audio, 24000, format="WAV")
    wav_io.seek(0)

    # Convert to MP3
    audio_segment = AudioSegment.from_wav(wav_io)
    audio_segment.export(output_path, format="mp3", bitrate="64k")

    # Return the relative path for the web app
    return os.path.join("static", "audio", output_filename_with_ext)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate audio from text file using Kokoro-TTS"
    )
    parser.add_argument("--input", "-i", required=True, help="Path to the input text file")
    parser.add_argument(
        "--output",
        "-o",
        default="static/audio",
        help="Output folder for the audio file",
    )
    parser.add_argument(
        "--filename",
        "-n",
        default="tts_audio",
        help="Output audio filename",
    )
    parser.add_argument("--voice", "-v", default="af_heart", help="Voice name")
    args = parser.parse_args()

    # Ensure the output directory exists
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    text = process_text_file(args.input)
    # The command line version will save to the specified folder
    # We update generate_audio slightly if needed but let's keep it simple for the web-first focus
    path = generate_audio(text, args.filename, voice=args.voice)
    print(f"Audio generated: {path}")


if __name__ == "__main__":
    main()
