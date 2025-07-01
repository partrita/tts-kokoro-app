import argparse
import os
from typing import List
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


def process_text_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    return text


def generate_audio(text: str, output_filename_no_ext: str) -> str:
    pipeline: KPipeline = KPipeline(lang_code="a")
    generator = pipeline(text, voice="af_heart", speed=1, split_pattern=r"\n+")

    all_audio: List[np.ndarray] = []

    for i, (gs, ps, audio) in enumerate(generator):
        all_audio.append(audio)

    # Concatenate all audio segments
    combined_audio: np.ndarray = np.concatenate(all_audio)

    # Construct the full output path, ensuring it's in the static directory
    # Assuming run.py is in app/, so static/ is at ../static/
    output_folder: str = os.path.join("..", "static")
    # Ensure the static directory exists, create if not (though ideally it should exist)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_filename_with_ext: str = output_filename_no_ext + ".mp3"
    output_path: str = os.path.join(output_folder, output_filename_with_ext)

    # Save the combined audio to a temporary WAV file in memory
    wav_io: io.BytesIO = io.BytesIO()
    sf.write(wav_io, combined_audio, 24000, format="WAV")
    wav_io.seek(0)

    # Convert WAV to MP3
    audio_segment: AudioSegment = AudioSegment.from_wav(wav_io)
    audio_segment.export(output_path, format="mp3", bitrate="64k")

    # Return the relative path for web serving
    return os.path.join("static", output_filename_with_ext)


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Generate audio from text file using Kokoro-TTS"
    )
    parser.add_argument("--input", "-i", help="Path to the input text file")
    parser.add_argument(
        "--output",
        "-o",
        default=".",
        help="Output folder for the audio file (default: current directory)",
    )
    parser.add_argument(
        "--filename",
        "-n",
        default="tts_audio",
        help="Output audio filename (default: tts_audio)",
    )
    args: argparse.Namespace = parser.parse_args()

    # Ensure the output directory exists
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    text: str = process_text_file(args.input)
    generate_audio(text, args.output, args.filename)


if __name__ == "__main__":
    main()
