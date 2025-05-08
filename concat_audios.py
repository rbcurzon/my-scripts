import sys
import os
import re
import pydub
from pathlib import Path

if __name__ == "__main__":

    parent = sys.argv[1] if len(sys.argv) > 1 else None
    if parent is None:
        print("Please provide the path to the directory containing the audio files.")
        sys.exit(1)
    if not os.path.isdir(parent):
        print(f"Provided path {parent} is not a directory.")
        sys.exit(1)

    p = Path(os.path.join(os.getcwd(),
                        parent))

    ptr1 = None
    ptr2 = None

    mp3s = sorted(p.rglob("*.mp3"),key=lambda x:float(re.findall("(\d+)",str(x))[0]))
    for file in mp3s:
        print("Appending", file)

        audio = pydub.AudioSegment.from_mp3(file)
        if ptr1 is None:
            ptr1 = audio
        else:
            ptr1 += audio

    output_path = os.path.join(os.getcwd(), "marcos", "output.mp3")
    if ptr1:
        ptr1.export(output_path, format="mp3")
        print(f"Saved to {output_path}")