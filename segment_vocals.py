import argparse
import os
from glob import glob

import multiprocessing
from pathlib import Path
from multiprocessing import Pool
from pydub import AudioSegment
from pydub.silence import split_on_silence
from concurrent.futures import ThreadPoolExecutor

def segment_vocals(input_file, output_dir, silence_thresh=-45, min_silence_len=800):
    """
    Segments vocals from an audio file and saves them as separate files.

    Parameters:
    - input_file: Path to the input audio file.
    - output_dir: Directory where segmented files will be saved.
    - silence_thresh: Silence threshold in dBFS (default: -45 dBFS).
    - min_silence_len: Minimum length of silence to consider (default: 800 ms).
    """
    # Load the audio file
    audio = AudioSegment.from_mp3(input_file)
    
    print(f"Processing {input_file}...")

    # Split the audio on silence
    segments = split_on_silence(audio, 
                                min_silence_len=min_silence_len, 
                                silence_thresh=silence_thresh)

    print(f"Found {len(segments)} segments.")

    #
    output_path = Path(output_dir) / input_file.split('/')[-2]

    if not Path(output_path).exists():
        Path(output_path).mkdir(parents=True, exist_ok=True)

    # Save each segment as a separate file
    for i, segment in enumerate(segments):
        segment.export(f"{output_path}/segment_{i}.mp3", format="mp3")

    print(f"Segments saved to {output_path}")

if __name__ == "__main__":

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Segment vocals from an audio file.")
    parser.add_argument("input_file", nargs='+', help="Path to one or more input audio files or a directory.")
    parser.add_argument("--output", help="Directory to save segmented files.")
    parser.add_argument("--silence_thresh", type=int, default=-45, help="Silence threshold in dBFS.")
    parser.add_argument("--min_silence_len", type=int, default=800, help="Minimum silence length in ms.")

    # Parse arguments
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    with ThreadPoolExecutor(max_workers=min(3, len(args.input_file))) as executor:
        futures = [
            executor.submit(segment_vocals, file, args.output, args.silence_thresh, args.min_silence_len)
            for file in args.input_file
        ]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred: {e}")