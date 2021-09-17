import pytest

from cato_server.api.schemas.run_schemas import ComparisonSettingsSchema


class TestComparisonSettingsSchema:
    def test_success(self):
        schema = ComparisonSettingsSchema()

        errors = schema.validate({"method": "SSIM", "threshold": 1})

        assert errors == {}

    @pytest.mark.parametrize(
        "data,expected_errors",
        [
            (
                {"method": "test", "threshold": 1},
                {"method": ["Invalid enum member test"]},
            ),
            (
                {"method": "SSIM", "threshold": "test"},
                {"threshold": ["Not a valid number."]},
            ),
            ({"threshold": 1}, {"method": ["Missing data for required field."]}),
            ({"method": "SSIM"}, {"threshold": ["Missing data for required field."]}),
        ],
    )
    def test_failure(self, data, expected_errors):
        schema = ComparisonSettingsSchema()

        errors = schema.validate(data)

        assert errors == expected_errors
