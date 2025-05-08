import sys
import math
from pydub import AudioSegment
from pydub.silence import split_on_silence
from spleeter.separator import Separator

if __name__ == "__main__":

    if (len(sys.argv) < 2):
        print("Please provide the audio file path as a command line argument.")
        sys.exit(1)

    audio = AudioSegment.from_mp3(sys.argv[1])

    segement_count = math.ceil(len(audio) / 3600000)

    for i in range(segement_count):
        start_time = i * 3600000
        end_time = min((i + 1) * 3600000, len(audio))
        segment = audio[start_time:end_time]
        segment.export(f"segment_{i}.mp3", format="mp3")
    
    separator = Separator('spleeter:2stems')
    for i in range(segement_count):
        separator.separate_to_file(f"segment_{i}.mp3", f"output/", codec='mp3', duration=3600)

    for i in range(segement_count):
        vocal_path = f"output/segment_{i}/vocals.mp3"
        audio = AudioSegment.from_mp3(vocal_path)
        silence_segments = split_on_silence(audio, min_silence_len=1000, silence_thresh=-45)
        
        for j, segment in enumerate(silence_segments):
            segment.export(f"output/segment_{i}/vocal_segment_{j}.mp3", format="mp3")