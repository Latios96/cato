import pytest

from cato_server.api.schemas.test_submission_schemas import SubmissionInfoSchema


class TestSubmissionInfoSchema:
    def test_success(self):
        data = {"run_id": 2, "resource_path": "some/path", "executable": "some/path"}
        schema = SubmissionInfoSchema()

        errors = schema.validate(data)

        assert errors == {}

    @pytest.mark.parametrize(
        "data,expected_errors",
        [
            (
                {},
                {
                    "executable": ["Missing data for required field."],
                    "resource_path": ["Missing data for required field."],
                    "run_id": ["Missing data for required field."],
                },
            ),
            (
                {"run_id": "test", "resource_path": "|", "executable": "|"},
                {
                    "executable": [
                        "invalid char found: invalids=('|'), value='|', "
                        "reason=INVALID_CHARACTER, target-platform=Windows"
                    ],
                    "resource_path": [
                        "invalid char found: invalids=('|'), value='|', "
                        "reason=INVALID_CHARACTER, target-platform=Windows"
                    ],
                    "run_id": ["Not a valid integer."],
                },
            ),
        ],
    )
    def test_failure_required_fields(self, data, expected_errors):
        schema = SubmissionInfoSchema()

        errors = schema.validate(data)

        assert errors == expected_errors
