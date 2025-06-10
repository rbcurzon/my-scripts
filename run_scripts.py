import sys
import threading
import subprocess
import multiprocessing as mp
from multiprocessing import Pool

def run_script(script_name, arg1):
    subprocess.run(["python3", script_name, arg1])

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Usage: python run_scripts.py <script_name> <url> <num_scripts>")
        sys.exit(1)

    with Pool(processes=mp.cpu_count() ) as pool:
        script_args = [
            (sys.argv[1],f"{sys.argv[2]}/{i}")
            for i in range(1, int(sys.argv[3]) + 1)
        ]
        results = pool.starmap(run_script, script_args)

    print("Scripts have finished executing.")