import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import List, Tuple

import cato


def _read_requirements():
    print("reading requirements..")
    requirements_path = Path(__file__).parent.parent / "requirements.txt"
    with open(requirements_path) as f:
        requirements = f.read().strip()
    requirements = requirements.split("\n")
    return map(lambda x: f"Requires-Dist: {x}\n", requirements)


def _remove_unused_modules(wheel_folder: Path, modules_to_keep: List[str]):
    print("removing unused modules..")
    folders = [f for f in wheel_folder.iterdir() if f.is_dir()]
    for folder in folders:
        if not ".dist-info" in folder.name and folder.name not in modules_to_keep:
            print(f"remove {folder}")
            shutil.rmtree(folder)


def _rename_dist_folder(target_folder: Path, new_name: str) -> Path:
    matches = list(target_folder.glob("cato-*.dist-info"))
    if not matches:
        raise ValueError("No METADATA file found for patching")
    dist_folder = matches[0]

    new_dist_folder = Path(str(dist_folder).replace("cato-", f"{new_name}-"))
    shutil.move(dist_folder, new_dist_folder)
    print(f"Renamed dist folder {dist_folder} -> {new_dist_folder}")

    return new_dist_folder


def _modify_entry_points(dist_folder: Path, entry_points_to_keep: List[str]):
    print("Modifying entry points..")
    with open(dist_folder / "entry_points.txt", "r") as f:
        entry_points = f.readlines()

    entry_points = list(
        filter(
            lambda x: x.startswith("[console_scripts]")
            or x.split("=")[0] in entry_points_to_keep,
            entry_points,
        )
    )

    with open(dist_folder / "entry_points.txt", "w") as f:
        f.writelines(entry_points)


def _modify_name_and_requirements(
    dist_folder: Path, new_name, requirements_to_keep: List[str]
):
    print("Modifying name and requirements..")
    with open(dist_folder / "METADATA", "r") as f:
        lines = f.readlines()

    lines += _read_requirements()

    processed_lines = []

    for line in lines:
        if line.startswith("Name: "):
            processed_lines.append(f"Name: {new_name}\n")
        elif line.startswith("Requires-Dist: "):
            package_name = line.split(" ")[1].strip()
            package_name = package_name.split("==")[0]
            if package_name in requirements_to_keep:
                processed_lines.append(line)
        else:
            processed_lines.append(line)

    with open(dist_folder / "METADATA", "w") as f:
        f.writelines(processed_lines)


def _modify_record(dist_folder: Path, modules_to_keep: List[str]):
    print("Modifying record..")
    with open(dist_folder / "RECORD", "r") as f:
        lines = f.readlines()

    lines = list(filter(lambda x: x.split("/")[0] in modules_to_keep, lines))

    with open(dist_folder / "RECORD", "w") as f:
        f.writelines(lines)


def _include_files(target_folder: Path, include_files: List[Tuple[Path, Path]] = None):
    if include_files:
        for src, dst in include_files:
            print(f"Copy {src} to {dst}")
            shutil.copy(src, target_folder / dst)


def create_new_wheel(
    path_to_wheel: Path,
    new_name: str,
    modules_to_keep: List[str],
    entry_points_to_keep: List[str],
    requirements_to_keep: List[str],
    include_files: List[Tuple[Path, Path]] = None,
):
    with tempfile.TemporaryDirectory() as tmpdirname:
        print("extracting original wheel..")
        with zipfile.ZipFile(path_to_wheel, "r") as zip_ref:
            target_folder = Path(tmpdirname)
            zip_ref.extractall(target_folder)

        _remove_unused_modules(target_folder, modules_to_keep)
        dist_folder = _rename_dist_folder(target_folder, new_name)
        _modify_entry_points(dist_folder, entry_points_to_keep)
        _modify_name_and_requirements(dist_folder, new_name, requirements_to_keep)
        _modify_record(dist_folder, modules_to_keep)
        _include_files(target_folder, include_files)

        path_to_new_wheel = path_to_wheel.parent / path_to_wheel.name.replace(
            "cato", new_name
        )
        print("creating new archive for wheel..")
        shutil.make_archive(path_to_new_wheel, "zip", tmpdirname)
        print("rename wheel..")
        shutil.move(str(path_to_new_wheel) + ".zip", path_to_new_wheel)


def find_current_wheel() -> Path:
    return find_wheel("cato")


def find_wheel(name) -> Path:
    current_version = cato.__version__
    return (
        Path(__file__).parent.parent
        / "dist"
        / f"{name}-{current_version}-py3-none-any.whl"
    )


if __name__ == "__main__":
    create_new_wheel(
        find_current_wheel(),
        new_name="cato-client",
        modules_to_keep=["cato", "cato_api_client", "cato_common"],
        entry_points_to_keep=["cato"],
        requirements_to_keep=[
            "python",
            "emoji",
            "pinject",
            "jsonschema",
            "contexttimer",
            "humanfriendly",
            "tabulate =",
            "py-cpuinfo",
            "psutil",
            "requests",
            "python-dateutil",
            "schedule",
            "sentry-sdk",
            "passlib",
            "case-converter",
            "itsdangerous",
            "tenacity",
            "pathvalidate",
            "tabulate",
            "email-validator",
            "Jinja2",
            "url-normalize",
            "matplotlib",
            "Pillow",
            "opencv-python-headless",
            "numpy",
            "scikit-image",
            "scipy",
            "pytracing",
            "flip",
        ],
    )

    create_new_wheel(
        find_current_wheel(),
        new_name="cato-server",
        modules_to_keep=["cato_server", "cato_common"],
        entry_points_to_keep=[
            "cato_worker",
            "cato_beat",
            "cato_server_admin",
            "db_load_generator",
        ],
        requirements_to_keep=[
            "python",
            "pinject",
            "contexttimer",
            "humanfriendly",
            "Jinja2",
            "alembic",
            "SQLAlchemy",
            "gevent",
            "marshmallow",
            "requests",
            "marshmallow-enum",
            "python-dateutil",
            "pathvalidate",
            "future",
            "schedule",
            "psycopg2-binary",
            "fastapi",
            "uvicorn",
            "aiofiles",
            "python-multipart",
            "Pillow",
            "opencv-python-headless",
            "sentry-sdk",
            "passlib",
            "email-validator",
            "numpy",
            "case-converter",
            "itsdangerous",
            "Authlib",
            "httpx",
            "starlette-csrf",
            "tenacity",
            "celery[rabbitmq]",
            "scikit-image",
            "cycler",
            "kiwisolver",
            "pytz",
            "pandas",
            "scipy",
            "imageio",
            "networkx",
            "tifffile",
            "pywavelets",
            "jsonschema",
            "jsonpath-ng",
            "marshmallow-polyfield",
            "matplotlib",
            "flip",
        ],
        include_files=[
            (
                find_wheel("cato-client"),
                Path("cato_server")
                / "static"
                / "static"
                / "cato-client-0.0.0-py3-none-any.whl",
            )
        ],
    )
