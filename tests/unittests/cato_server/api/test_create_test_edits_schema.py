from cato_server.api.schemas.create_test_edits_schemas import (
    CreateComparisonSettingsEditSchema,
)


class TestCreateComparisonSettingsEditSchema:
    def test_success(self):
        data = {"testResultId": 1, "newValue": {"method": "SSIM", "threshold": 1}}
        schema = CreateComparisonSettingsEditSchema()

        errors = schema.validate(data)

        assert errors == {}

    def test_failure(self):
        data = {"testResultId": 1, "newValue": {"method": "SSIM", "thredshold": 1}}
        schema = CreateComparisonSettingsEditSchema()

        errors = schema.validate(data)

        assert errors == {
            "newValue": {"threshold": ["Missing data for required field."]}
        }
