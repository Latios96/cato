import pytest

from cato_common.domain.project import Project, ProjectStatus
from cato_server.configuration.app_configuration_defaults import (
    AppConfigurationDefaults,
)
from cato_server.images.oiio_binaries_discovery import OiioBinariesDiscovery
from cato_server.images.oiio_command_executor import OiioCommandExecutor
from cato_server.usecases.create_project_image import CreateProjectImage


def test_create_project_image(
    test_resource_provider,
    project,
    sqlalchemy_project_repository,
    sqlalchemy_deduplicating_storage,
):
    AppConfigurationDefaults().create(),
    create_project_image = CreateProjectImage(
        sqlalchemy_project_repository,
        sqlalchemy_deduplicating_storage,
        OiioBinariesDiscovery(),
        OiioCommandExecutor(),
        AppConfigurationDefaults().create(),
    )

    assert project.thumbnail_file_id is None

    with open(
        test_resource_provider.resource_by_name("test_image_white.jpg"), "rb"
    ) as f:
        project = create_project_image.create_project_image(project, f, "test.jpg")

    assert project.thumbnail_file_id == 1


def test_create_project_image_should_fail_unsupported_format(
    test_resource_provider,
    project,
    sqlalchemy_project_repository,
    sqlalchemy_deduplicating_storage,
):
    AppConfigurationDefaults().create(),
    create_project_image = CreateProjectImage(
        sqlalchemy_project_repository,
        sqlalchemy_deduplicating_storage,
        OiioBinariesDiscovery(),
        OiioCommandExecutor(),
        AppConfigurationDefaults().create(),
    )

    assert project.thumbnail_file_id is None

    with open(
        test_resource_provider.resource_by_name("test_image_white.jpg"), "rb"
    ) as f:  #
        with pytest.raises(ValueError):
            project = create_project_image.create_project_image(project, f, "test.txt")
