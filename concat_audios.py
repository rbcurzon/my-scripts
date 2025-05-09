import sys
import os
import re
import pydub
from pathlib import Path

if __name__ == "__main__":

    split_vocals_path = sys.argv[1] if len(sys.argv) > 1 else None

    if split_vocals_path is None:
        print("Please provide the path to the directory containing the audio files.")
        sys.exit(1)
    if not os.path.isdir(split_vocals_path):
        print(f"Provided path {split_vocals_path} is not a directory.")
        sys.exit(1)

    p = Path(split_vocals_path)

    ptr1 = None

    try:
        mp3s = sorted(p.rglob("*.mp3"),key=lambda x:float(re.findall(r"\d+",str(Path(x).stem))[0]))
    except Exception as e:
        print(f"Error while searching for mp3 files: {e}")
        sys.exit(1)

    print(mp3s)
    for file in mp3s:
        print("Appending", file)

        audio = pydub.AudioSegment.from_mp3(file)
        if ptr1 is None:
            ptr1 = audio
        else:
            ptr1 += audio

    output_path = os.path.join(p, "combined.mp3")

    if ptr1:
        ptr1.export(output_path, format="mp3")
        print(f"Saved to {output_path}")