import os
import sys
import math
from pydub import AudioSegment
from pydub.silence import split_on_silence
from multiprocessing import Pool

# from spleeter.separator import Separator

# separator = Separator('spleeter:2stems')

def process_segment(audio_file, segment):
    i = segment
    start_time = i * 3600000
    end_time = min((i + 1) * 3600000, len(audio))
    segment = audio[start_time:end_time]
    print(f"Processing segment {i} from {start_time} to {end_time}")
    segment.export(f"segment_{i}.mp3", format="mp3")

if __name__ == "__main__":

    if (len(sys.argv) < 2):
        print("Please provide the audio file path as a command line argument.")
        sys.exit(1)

    audio = AudioSegment.from_file(sys.argv[1], format="m4a")

    segement_count = math.ceil(len(audio) / 3600000)

    print("Segment count: ", segement_count)

    # Put the audio in batch of 1 hour
    with Pool(processes=2) as pool:
        pool.starmap(process_segment, [(sys.argv[1], i) for i in range(segement_count)])


    # # Separate vocals from each segment
    # for i in range(segement_count):
    #     separator.separate_to_file(f"segment_{i}.mp3", 
    #                                f"output/", 
    #                                duration=3600,
    #                                codec='mp3')
        
    # concatenated_audio = AudioSegment.empty()

    # # Concatenate the separated vocals
    # for i in range(segement_count):
    #     if os.path.isfile(f"segment_{i}.mp3"):
    #         os.remove(f"segment_{i}.mp3")
    #     concatenated_audio += AudioSegment.from_mp3(f"output/segment_{i}/vocals.mp3")
    
    # output_path = os.path.join("output", "combined_vocals.mp3")
    # concatenated_audio.export(output_path, format="mp3")

    # # Segement audio in silence
    # silence_segments = split_on_silence(output_path, 
    #                                     min_silence_len=800, 
    #                                     silence_thresh=-45)
    
    # for i, segment in enumerate(silence_segments):
    #     segment.export(f"output/chunks/silence_segment_{i}.mp3", format="mp3")
    
    # combined_vocals = AudioSegment.from_mp3(f"output/combined_vocals.mp3")
    
    