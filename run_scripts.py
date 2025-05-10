import threading
import subprocess
from multiprocessing import Pool

import sys

def run_script(script_name, arg1):
    subprocess.run(["python", script_name, arg1])

if __name__ == "__main__":
    with Pool(processes=2) as pool:
        script_args = [
            (sys.argv[1],f"{sys.argv[2]}/{i}")
            for i in range(1, int(sys.argv[3]) + 1)
        ]
        pool.starmap(run_script, script_args)

    print("Scripts have finished executing.")