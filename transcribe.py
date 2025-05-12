
import multiprocessing
multiprocessing.set_start_method('spawn', force=True)

import sys
import csv
from pathlib import Path
from multiprocessing import Pool
import whisper

model = whisper.load_model("large")

def transcribe_segments(segment_path):
    """
    Transcribe the given audio file using the Whisper model.
    """
    
    segment_path = Path(segment_path)

    if segment_path.is_dir():
        # If the path is a directory, get all mp3 files in it
        files = Path(segment_path).glob("*.mp3")
        metadata_path = segment_path / "metadata.csv"
    elif segment_path.is_file() and segment_path.suffix == ".mp3":
        files = [segment_path]
        metadata_path = segment_path.parent / "metadata.csv"
    else:
        print(f"Invalid path: {segment_path}. Please provide a directory or an mp3 file.")
        return

    print(f"Transcribing {segment_path}...")
    
    with open(metadata_path, "w") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(["file_name", "transcription"])

        for audio_file in files:
            # Transcribe the audio file
            result = model.transcribe(str(audio_file), language="tl", task="transcribe")
            writer.writerow([audio_file.name, result['text']])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <audio_file/s>")
        sys.exit(1)

    with Pool(processes=2) as p:
        p.map(transcribe_segments, sys.argv[1:])
        p.close()
        p.join()

    print("Transcription completed.")