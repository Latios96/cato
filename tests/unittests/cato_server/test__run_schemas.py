import pytest

from cato_server.api.schemas.run_schemas import (
    ComparisonSettingsSchema,
    RunBatchIdentifierSchema,
)


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


class TestRunBatchIdentifierSchema:
    def test_success(self):
        schema = RunBatchIdentifierSchema()

        errors = schema.validate(
            {
                "provider": "LOCAL_COMPUTER",
                "runName": "mac-os",
                "runIdentifier": "3046812908-1",
            }
        )

        assert errors == {}

    @pytest.mark.parametrize(
        "data,expected_errors",
        [
            (
                {
                    "provider": "SOMEWHERE",
                    "runName": "mac-os",
                    "runIdentifier": "3046812908-1",
                },
                {"provider": ["Invalid enum member SOMEWHERE"]},
            ),
            (
                {
                    "runName": "mac-os",
                    "runIdentifier": "3046812908-1",
                },
                {"provider": ["Missing data for required field."]},
            ),
            (
                {
                    "provider": "LOCAL_COMPUTER",
                    "runName": "",
                    "runIdentifier": "3046812908-1",
                },
                {"runName": ["Shorter than minimum length 1."]},
            ),
            (
                {
                    "provider": "LOCAL_COMPUTER",
                    "runName": None,
                    "runIdentifier": "3046812908-1",
                },
                {"runName": ["Field may not be null."]},
            ),
            (
                {
                    "provider": "LOCAL_COMPUTER",
                    "runName": "mac-os",
                    "runIdentifier": "",
                },
                {"runIdentifier": ["Shorter than minimum length 1."]},
            ),
            (
                {
                    "provider": "LOCAL_COMPUTER",
                    "runName": "mac-os",
                    "runIdentifier": None,
                },
                {"runIdentifier": ["Field may not be null."]},
            ),
        ],
    )
    def test_failure(self, data, expected_errors):
        schema = RunBatchIdentifierSchema()

        errors = schema.validate(data)

        assert errors == expected_errors
