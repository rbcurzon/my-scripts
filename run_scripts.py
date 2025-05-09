import threading
import subprocess
import sys

def run_script(script_name, arg1):
    subprocess.run(["python", script_name, arg1])

if __name__ == "__main__":

    
    first = sys.argv[1]
    last = sys.argv[2]

    thread_list = []
    for i in range(1, int(last) + 1, 3):
        thread = threading.Thread(target=run_script, args=(
            f"../scrape_audio.py",
            f"https://live.bible.is/bible/PAGPBS/MRK/{i}?audio_type=audio_drama"
            ))
        thread_list.append(thread)
        thread.start()

    # Wait for all threads to complete

    for thread in thread_list:
        thread.join()

    print("Scripts have finished executing.")