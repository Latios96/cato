import shutil
import sys

if __name__ == "__main__":
    print(f"Copy {sys.argv[1]} to {sys.argv[2]}")
    shutil.copy(sys.argv[1], sys.argv[2])
