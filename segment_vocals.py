from pathlib import Path
from multiprocessing import Pool
from pydub import AudioSegment
from pydub.silence import split_on_silence

def segment_vocals(input_file, output_dir, silence_thresh=-50, min_silence_len=800):
    """
    Segments vocals from an audio file and saves them as separate files.

    Parameters:
    - input_file: Path to the input audio file.
    - output_dir: Directory where segmented files will be saved.
    - silence_thresh: Silence threshold in dBFS (default: -50 dBFS).
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

    output_path = os.path.join(output_dir, Path(input_file).stem)

    if not Path.exists(output_path):
        Path(output_path).mkdir(parents=True, exist_ok=True)

    # Save each segment as a separate file
    for i, segment in enumerate(segments):
        segment.export(f"{output_dir}/segment_{i}.mp3", format="mp3")

if __name__ == "__main__":
    import argparse
    import os
    from glob import glob

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Segment vocals from an audio file.")
    parser.add_argument("input_file", help="Path to the input audio file.")
    parser.add_argument("output_dir", help="Directory to save segmented files.")
    parser.add_argument("--silence_thresh", type=int, default=-50, help="Silence threshold in dBFS.")
    parser.add_argument("--min_silence_len", type=int, default=800, help="Minimum silence length in ms.")

    # Parse arguments
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    with Pool(processes=2) as pool:
        # Get a list of all audio files in the input directory
        input_files = [args.input_file] if Path(args.input_file).is_file() else glob(args.input_file)

        # Prepare arguments for parallel processing
        tasks = [(file, args.output_dir, args.silence_thresh, args.min_silence_len) for file in input_files]

        # Process files in parallel
        pool.starmap(segment_vocals, tasks)