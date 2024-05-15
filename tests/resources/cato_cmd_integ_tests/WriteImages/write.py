import os
import sys

from PIL import Image

if __name__ == "__main__":
    color = (255, 255, 255) if sys.argv[2] == "white" else (0, 0, 0)
    resolution = (
        (800, 600) if len(sys.argv) == 3 else (int(sys.argv[3]), int(sys.argv[4]))
    )
    img = Image.new(
        "RGB",
        resolution,
    )
    directory = os.path.dirname(sys.argv[1])
    if not os.path.exists(directory):
        os.makedirs(directory)
    img.save(sys.argv[1], "PNG")
    pass
