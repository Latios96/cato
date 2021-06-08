import pytest

from cato_server.storage.abstract.project_repository import ProjectRepository
from cato_server.api.validators.project_validators import CreateProjectValidator
from tests.utils import mock_safe


class TestCreateProjectValidator:
    @pytest.mark.parametrize(
        "project_name",
        [
            "my_project_name",
            "my-project_name",
            "my-project_name222",
            "22",
            "My-Project-Name",
            "My-Project Name",
        ],
    )
    def test_valid_name(self, project_name):
        mock_project_repo = mock_safe(ProjectRepository)
        mock_project_repo.find_by_name.return_value = None
        project_validator = CreateProjectValidator(mock_project_repo)

        errors = project_validator.validate({"name": project_name})

        assert not errors

    @pytest.mark.parametrize(
        "invalid_project_name,error_messages",
        [
            ("myinvalid%name", ["String does not match expected pattern."]),
            ("myinvalid$name", ["String does not match expected pattern."]),
            ("myinvalid§*+*name", ["String does not match expected pattern."]),
            ("myinvalid/name", ["String does not match expected pattern."]),
            ("myinvalid\\name", ["String does not match expected pattern."]),
            ("my invalid&name", ["String does not match expected pattern."]),
            (
                "",
                [
                    "Shorter than minimum length 1.",
                    "String does not match expected pattern.",
                ],
            ),
        ],
    )
    def test_invalid_name(self, invalid_project_name, error_messages):
        mock_project_repo = mock_safe(ProjectRepository)
        mock_project_repo.find_by_name.return_value = None
        project_validator = CreateProjectValidator(mock_project_repo)

        errors = project_validator.validate({"name": invalid_project_name})

        assert errors == {"name": error_messages}

    def test_same_name_should_fail(self):
        mock_project_repo = mock_safe(ProjectRepository)
        mock_project_repo.find_by_name.return_value = True
        project_validator = CreateProjectValidator(mock_project_repo)

        errors = project_validator.validate({"name": "project_name"})

        assert errors == {"name": ['Project with name "project_name" already exists!']}
