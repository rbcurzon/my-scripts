import threading
import subprocess
import sys

def run_script(script_name, arg1):
    subprocess.run(["python", script_name, arg1])

if __name__ == "__main__":

    book_chapter_count = sys.argv[1] if len(sys.argv) > 1 else 1

    thread_list = []
    for i in range(1, int(book_chapter_count) + 1):
        thread = threading.Thread(target=run_script, args=(
            f"scrape_audio.py",
            f"https://live.bible.is/bible/MRWNVS/MRK/{i}?audio_type=audio_drama"
            ))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

    print("Scripts have finished executing.")