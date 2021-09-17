from cato_server.api.schemas.create_test_edits_schemas import (
    CreateComparisonSettingsEditSchema,
)


class TestCreateComparisonSettingsEditSchema:
    def test_success(self):
        data = {"test_result_id": 1, "new_value": {"method": "SSIM", "threshold": 1}}
        schema = CreateComparisonSettingsEditSchema()

        errors = schema.validate(data)

        assert errors == {}

    def test_failure(self):
        data = {"test_result_id": 1, "new_value": {"method": "SSIM", "thredshold": 1}}
        schema = CreateComparisonSettingsEditSchema()

        errors = schema.validate(data)

        assert errors == {
            "new_value": {"threshold": ["Missing data for required field."]}
        }
