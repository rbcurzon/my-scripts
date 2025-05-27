import threading
import subprocess
from multiprocessing import Pool

import sys

def run_script(script_name, arg1):
    subprocess.run(["python", script_name, arg1])

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Usage: python run_scripts.py <script_name> <output_dir> <num_scripts>")
        sys.exit(1)

    with Pool(processes=2) as pool:
        script_args = [
            (sys.argv[1],f"{sys.argv[2]}/{i}")
            for i in range(1, int(sys.argv[3]) + 1)
        ]
        results = pool.starmap(run_script, script_args)

    print("Scripts have finished executing.")