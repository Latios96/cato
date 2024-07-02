import subprocess
import sys
import tempfile
from pathlib import Path

import cato


def find_wheel(name: str) -> Path:
    current_version = cato.__version__
    return (
        Path(__file__).parent.parent
        / "dist"
        / f"{name}-{current_version}-py3-none-any.whl"
    )


class Venv:
    def __init__(self, path: Path):
        self._base_path = path

    def run_pip(self, args):
        self.run_executable("pip", args)

    def run_executable(self, exe_name, args):
        print(f"Running {exe_name} with {args}")
        executable = self._executable_dir / exe_name
        command = [str(executable), *args]
        subprocess.call(command)

    @property
    def _executable_dir(self):
        if sys.platform == "win32":
            return self._base_path / "Scripts"
        return self._base_path / "bin"


def create_virtual_env(folder: Path) -> Venv:
    print(f"Creating virtualenv at {folder}")
    command = [sys.executable, "-m", "virtualenv", str(folder)]
    subprocess.call(command)
    return Venv(folder)


def check_cato_server_wheel():
    with tempfile.TemporaryDirectory() as tmpdirname:
        venv = create_virtual_env(Path(tmpdirname))
        venv.run_pip(["install", str(find_wheel("catoserver"))])
        venv.run_executable("python", ["-m", "cato_server", "-h"])
        venv.run_executable("cato_beat", ["-h"])
        venv.run_executable("cato_worker", ["-h"])
        venv.run_executable("cato_server_admin", ["-h"])


def check_cato_client_wheel():
    with tempfile.TemporaryDirectory() as tmpdirname:
        venv = create_virtual_env(Path(tmpdirname))
        venv.run_pip(["install", str(find_wheel("catoclient"))])
        venv.run_executable("cato", ["-h"])


if __name__ == "__main__":
    check_cato_server_wheel()
    check_cato_client_wheel()
