import sys

from PIL import Image

if __name__ == "__main__":
    color = (255, 255, 255) if sys.argv[2] == "white" else (0, 0, 0)
    img = Image.new(
        "RGB",
        (800, 600),
    )
    img.save(sys.argv[1], "PNG")
    pass
