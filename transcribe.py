import argparse
import csv
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
from pathlib import Path

import whisper
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset

model = whisper.load_model("turbo")


device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "openai/whisper-large-v3-turbo"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    torch_dtype=torch_dtype,
    device=device,
)

def transcribe_segments(segment_path, batch_size=8):
    segment_path = Path(segment_path)
    if segment_path.is_dir():
        files = list(Path(segment_path).glob("*.mp3"))
        metadata_path = segment_path / "metadata.csv"
    elif segment_path.is_file() and segment_path.suffix == ".mp3":
        files = [segment_path]
        metadata_path = segment_path.parent / "metadata.csv"
    else:
        logger.error(f"Invalid path: {segment_path}. Please provide a directory or an mp3 file.")
        return
    logger.info(f"Transcribing files in {segment_path}...")

    generate_kwargs={"batch_size": batch_size, "chunk_length_s": 30}

    paths_in_str = [str(file) for file in files]
    results = pipe(paths_in_str, **generate_kwargs)
    result_texts = [result["text"] for result in results]
    zip_results = zip(paths_in_str, result_texts)

    with open(metadata_path, "w") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(["file_name", "transcription"])
        writer.writerows(tuple(zip_results))
        logger.info(f"Finished transcribing {segment_path}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe audio files.")
    parser.add_argument("audio_files", nargs="+", help="List of audio files or directories to transcribe.")
    parser.add_argument("--batch_size", type=int, default=8, help="Batch size for transcription.")
    args = parser.parse_args()

    for file in args.audio_files:
        transcribe_segments(file, batch_size=args.batch_size)

    logger.info("Transcription completed.")