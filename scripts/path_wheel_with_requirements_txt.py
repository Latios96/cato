import os
import shutil
import tempfile
import zipfile
from pathlib import Path

import cato


def _read_requirements():
    print("reading requirements..")
    requirements_path = Path(__file__).parent.parent / "requirements.txt"
    with open(requirements_path) as f:
        requirements = f.read().strip()
    requirements = requirements.split("\n")
    return map(lambda x: f"Requires-Dist: {x}", requirements)


def patch_wheel(path_to_wheel):
    requirements = _read_requirements()

    with tempfile.TemporaryDirectory() as tmpdirname:
        print("extracting wheel..")
        with zipfile.ZipFile(path_to_wheel, "r") as zip_ref:
            target_folder = Path(tmpdirname)
            zip_ref.extractall(target_folder)

        matches = list(target_folder.glob("cato-*.dist-info/METADATA"))
        if not matches:
            raise ValueError("No METADATA file found for patching")
        match = matches[0]

        with open(match, "r") as f:
            original_data = f.read()
        original_data += "\n".join(requirements)

        print("patching METADATA..")
        with open(match, "w") as f:
            f.write(original_data)

        patched_wheel = os.path.join(tmpdirname, "patched_wheel")
        print("creating archive..")
        shutil.make_archive(patched_wheel, "zip", tmpdirname)
        patched_wheel += ".zip"
        os.remove(path_to_wheel)
        print("copy archive..")
        shutil.copy(patched_wheel, path_to_wheel)
        print("done.")


def find_current_wheel():
    current_version = cato.__version__
    return (
        Path(__file__).parent.parent
        / "dist"
        / f"cato-{current_version}-py3-none-any.whl"
    )


if __name__ == "__main__":
    patch_wheel(find_current_wheel())
