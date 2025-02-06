import argparse
import os
from typing import List, Tuple
from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
import numpy as np
from pydub import AudioSegment
import io

def process_text_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def generate_audio(text: str, output_folder: str, output_filename: str) -> None:
    pipeline: KPipeline = KPipeline(lang_code='a')
    generator = pipeline(
        text, voice='af_heart',
        speed=1, split_pattern=r'\n+'
    )

    all_audio: List[np.ndarray] = []

    for i, (gs, ps, audio) in enumerate(generator):
        all_audio.append(audio)

    # Concatenate all audio segments
    combined_audio: np.ndarray = np.concatenate(all_audio)

    # Construct the full output path
    output_path: str = os.path.join(output_folder, output_filename)

    # Save the combined audio to a temporary WAV file in memory
    wav_io: io.BytesIO = io.BytesIO()
    sf.write(wav_io, combined_audio, 24000, format='WAV')
    wav_io.seek(0)

    # Convert WAV to MP3
    audio_segment: AudioSegment = AudioSegment.from_wav(wav_io)
    audio_segment.export(output_path + ".mp3", format="mp3", bitrate="64k")

    print(f"Audio saved to: {output_path}.mp3!")

def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="Generate audio from text file using KPipeline")
    parser.add_argument("--input", "-i", help="Path to the input text file")
    parser.add_argument("--output", "-o", default=".", help="Output folder for the audio file (default: current directory)")
    parser.add_argument("--filename", "-n", default="tts_audio", help="Output audio filename (default: tts_audio)")
    args: argparse.Namespace = parser.parse_args()

    # Ensure the output directory exists
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    text: str = process_text_file(args.input)
    generate_audio(text, args.output, args.filename)

if __name__ == "__main__":
    main()
