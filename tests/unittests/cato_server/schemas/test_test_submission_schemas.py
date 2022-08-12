import pytest

from cato_server.api.schemas.test_submission_schemas import (
    SubmissionInfoSchema,
    ConfigSchema,
)
from tests.unittests.cato_common.config.test_config_file_parser import (
    INVALID_CONFIG,
    VALID_CONFIG,
    VALID_CONFIG_WITH_VARIABLES,
    VALID_CONFIG_WITH_VARIABLES_IN_SUITE_AND_TEST,
)


class TestSubmissionInfoSchema:
    def test_success(self):
        data = {
            "config": VALID_CONFIG,
            "runId": 2,
            "resourcePath": "some/path",
            "executable": "some/path",
        }
        schema = SubmissionInfoSchema()

        errors = schema.validate(data)

        assert errors == {}

    @pytest.mark.parametrize(
        "data,expected_errors",
        [
            (
                {},
                {
                    "config": ["Missing data for required field."],
                    "executable": ["Missing data for required field."],
                    "resourcePath": ["Missing data for required field."],
                    "runId": ["Missing data for required field."],
                },
            )
        ],
    )
    def test_failure_required_fields(self, data, expected_errors):
        schema = SubmissionInfoSchema()

        errors = schema.validate(data)

        assert errors == expected_errors


class TestConfigSchema:
    @pytest.mark.parametrize(
        "config",
        [
            VALID_CONFIG,
            VALID_CONFIG_WITH_VARIABLES,
            VALID_CONFIG_WITH_VARIABLES_IN_SUITE_AND_TEST,
        ],
    )
    def test_success(self, config):
        schema = ConfigSchema()

        errors = schema.validate(config)

        assert errors == {}

    @pytest.mark.parametrize("config", [INVALID_CONFIG])
    def test_failure(self, config):
        schema = ConfigSchema()

        errors = schema.validate(config)

        assert errors == {
            "projectName": ["Missing data for required field."],
            "suites": ["Missing data for required field."],
        }
