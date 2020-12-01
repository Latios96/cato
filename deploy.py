import os
import shutil
import subprocess

import git


def check_tag():
    repo = git.Repo(os.path.dirname(__file__))
    for tag in repo.tags:
        if tag.commit == repo.head.commit:
            return tag
    return None


def main():
    tag = check_tag()
    if not tag:
        print("Current commit is not tagged! Please run bumpversion!")
    version = tag.name[1:]
    print(f"Deploy version {version}..")

    print("Building..")
    subprocess.check_call("gradlew.bat build")

    print("Copy wheel..")
    wheel_path = os.path.join(
        os.path.dirname(__file__), "dist", f"cato-{version}-py3-none-any.whl"
    )
    shutil.copy(wheel_path, os.path.join(r'M:\cato\wheels', os.path.basename(wheel_path)))

    pip_path = r"M:\cato\venv\Scripts\pip"

    print("Install OpenImageIO..")
    subprocess.check_call(
        [
            pip_path,
            "install",
            "-r",
            os.path.join(os.path.dirname(__file__), "oiio-requirements.txt"),
        ]
    )

    print("Install..")
    subprocess.check_call([pip_path, "install", "--upgrade", wheel_path])

    print("Copy config..")
    prod_config = r"M:\cato\config.ini"
    prod_config_target = r"M:\cato\venv\Lib\site-packages\cato\storage\sqlalchemy\config.ini"
    shutil.copy(prod_config, prod_config_target)

    print("Done.")

if __name__ == "__main__":
    main()
