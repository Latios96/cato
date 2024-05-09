import os
import tempfile
import uuid
from typing import IO

from cato_common.domain.project import Project
from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.images.oiio_binaries_discovery import OiioBinariesDiscovery
from cato_server.images.oiio_command_executor import OiioCommandExecutor
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.project_repository import ProjectRepository


class CreateProjectImage:

    def __init__(
        self,
        project_repository: ProjectRepository,
        file_storage: AbstractFileStorage,
        oiio_binaries_discovery: OiioBinariesDiscovery,
        oiio_command_executor: OiioCommandExecutor,
        app_configuration: AppConfiguration,
    ):
        self._project_repository = project_repository
        self._file_storage = file_storage
        self._oiio_binaries_discovery = oiio_binaries_discovery
        self._oiio_command_executor = oiio_command_executor
        self._app_configuration = app_configuration

    def create_project_image(
        self, project: Project, image_stream: IO, image_name: str
    ) -> Project:
        with tempfile.TemporaryDirectory() as tmpdirname:
            _, ext = os.path.splitext(image_name)
            if ext not in {".jpg", ".jpeg", ".png", ".exr"}:
                raise ValueError("Unsupported image format")

            thumbnail_source_file = os.path.join(
                tmpdirname, f"thumbnail_source_{uuid.uuid4()}"
            )

            with open(thumbnail_source_file, "wb") as f:
                f.write(image_stream.read())

            thumbnail_target_path = os.path.join(
                tmpdirname, f"thumbnail_{uuid.uuid4()}.png"
            )
            thread_count = self._app_configuration.oiio_configuration.thread_count
            command = f"{self._oiio_binaries_discovery.get_oiiotool_executable()} --threads {thread_count} -i {thumbnail_source_file} --resize 300x0 -o {thumbnail_target_path}"
            self._oiio_command_executor.execute_command(command)
            if not os.path.exists(thumbnail_target_path):
                raise RuntimeError(
                    f"No thumbnail was created at path {thumbnail_target_path}"
                )
            thumbnail_file = self._file_storage.save_file(thumbnail_target_path)

        project.thumbnail_file_id = thumbnail_file.id
        self._project_repository.save(project)
        return project
