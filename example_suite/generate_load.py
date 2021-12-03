import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

MAX_CONCURRENT = 4


def run():
    for i in range(10):
        command = "python -m cato run -u 127.0.0.1:5000"
        print(command)
        subprocess.check_call(command)
        print("startd")

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as e:
        for i in range(MAX_CONCURRENT):
            e.submit(run)

        e.shutdown()