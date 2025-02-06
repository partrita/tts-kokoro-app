import argparse
import os
from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
import numpy as np

def process_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def generate_audio(text, output_folder, output_filename):
    pipeline = KPipeline(lang_code='a')
    generator = pipeline(
        text, voice='af_heart',
        speed=1, split_pattern=r'\n+'
    )

    all_audio = []

    for i, (gs, ps, audio) in enumerate(generator):
        all_audio.append(audio)

    # Concatenate all audio segments
    combined_audio = np.concatenate(all_audio)

    # Construct the full output path
    output_path = os.path.join(output_folder, output_filename)

    # Save the combined audio to the specified file
    sf.write(output_path + ".wav", combined_audio, 24000)

    print(f"Audio saved to: {output_path}.wav!")


def main():
    parser = argparse.ArgumentParser(description="Generate audio from text file using KPipeline")
    parser.add_argument("--input", "-i", help="Path to the input text file")
    parser.add_argument("--output", "-o", default=".", help="Output folder for the audio file (default: current directory)")
    parser.add_argument("--filename", "-n", default="tts_audio", help="Output audio filename (default: tts_audio)")
    args = parser.parse_args()

    # Ensure the output directory exists
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    text = process_text_file(args.input)
    generate_audio(text, args.output, args.filename)

if __name__ == "__main__":
    main()

