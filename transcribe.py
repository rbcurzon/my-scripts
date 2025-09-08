import argparse
import csv
from pathlib import Path

import whisper

model = whisper.load_model("turbo")

def transcribe_segments(segment_path):
    segment_path = Path(segment_path)
    if segment_path.is_dir():
        files = Path(segment_path).glob("*.mp3")
        metadata_path = segment_path / "metadata.csv"
    elif segment_path.is_file() and segment_path.suffix == ".mp3":
        files = [segment_path]
        metadata_path = segment_path.parent / "metadata.csv"
    else:
        print(f"Invalid path: {segment_path}. Please provide a directory or an mp3 file.")
        return

    print(f"Finished transcribing {segment_path}.")
    
    with open(metadata_path, "w") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(["file_name", "transcription"])

        for audio_file in files:
            # Transcribe the audio file
            result = model.transcribe(str(audio_file), language="tl", task="transcribe")
            writer.writerow([audio_file.name, result['text']])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio files.")
    parser.add_argument("audio_files", nargs="+", help="List of audio files or directories to transcribe.")
    args = parser.parse_args()

    for file in args.audio_files:
        transcribe_segments(file)

    print("Transcription completed.")