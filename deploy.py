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
        exit(1)
    version = tag.name[1:]

    print(f"Deploy version {version}..")

    static_path = os.path.join("cato_server", "static")
    if os.path.exists(static_path):
        print("Clean frontend")
        shutil.rmtree("cato_server/static")

    print("Building..")
    subprocess.check_call("gradlew.bat build -x pythonUnittest -x pythonIntegrationtest")

    print("Copy wheel..")
    wheel_path = os.path.join(
        os.path.dirname(__file__), "dist", f"catoserver-{version}-py3-none-any.whl"
    )
    shutil.copy(
        wheel_path, os.path.join(r"M:\cato\wheels", os.path.basename(wheel_path))
    )

    pip_path = r"M:\cato\venv\Scripts\pip"

    print("Install OpenImageIO..")
    subprocess.check_call(
        [
            pip_path,
            "install",
            "-r",
            os.path.join(os.path.dirname(__file__), "requirements.txt"),
        ]
    )

    print("Install..")
    subprocess.check_call([pip_path, "install", "--upgrade", wheel_path])

    print("Done.")


if __name__ == "__main__":
    main()
