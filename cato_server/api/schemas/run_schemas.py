from marshmallow import Schema, fields, EXCLUDE
from marshmallow.validate import Length
from marshmallow_enum import EnumField
from marshmallow_polyfield import PolyField

from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.run_batch_provider import RunBatchProvider
from cato_common.domain.run_information import OS, GithubActionsRunInformation
from cato_server.api.schemas.general import (
    ID_FIELD,
    NAME_FIELD,
    VARIABLES_FIELD,
)
from cato_server.api.schemas.test_result_schemas import is_test_identifier


class ComparisonSettingsSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    method = EnumField(ComparisonMethod, required=True)
    threshold = fields.Float(min=0, required=True)


class TestForRunCreationSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    testName = NAME_FIELD
    testIdentifier = fields.String(
        required=True, validate=[Length(min=3), is_test_identifier]
    )
    testCommand = fields.String(required=True, validate=[Length(1)])
    testVariables = VARIABLES_FIELD
    comparisonSettings = fields.Nested(ComparisonSettingsSchema, required=True)


class TestSuiteForRunCreationSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    suiteName = NAME_FIELD
    suiteVariables = VARIABLES_FIELD
    tests = fields.List(fields.Nested(TestForRunCreationSchema), required=True)


class RunBatchIdentifierSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    provider = EnumField(RunBatchProvider, required=True)
    runName = fields.String(validate=[Length(min=1)], required=True, allow_none=False)
    runIdentifier = fields.String(
        validate=[Length(min=1)], required=True, allow_none=False
    )


class BasicRunInformationSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    os = EnumField(OS, required=True, allow_none=False)
    computerName = fields.String(
        validate=[Length(min=1)], required=True, allow_none=False
    )
    runInformationType = EnumField(RunBatchProvider, required=True, allow_none=False)


class LocalRunInformationSchema(BasicRunInformationSchema):
    localUsername = fields.String(
        validate=[Length(min=1)], required=True, allow_none=False
    )


class GithubActionsRunInformationSchema(BasicRunInformationSchema):
    githubRunId = fields.Integer(min=1, required=True, allow_none=False)
    jobId = fields.Integer(min=1, required=True, allow_none=False)
    jobName = fields.String(validate=[Length(min=1)], required=True, allow_none=False)
    actor = fields.String(validate=[Length(min=1)], required=True, allow_none=False)
    attempt = fields.Integer(min=1, required=True, allow_none=False)
    runNumber = fields.Integer(min=1, required=True, allow_none=False)
    githubUrl = fields.Url(required=True, allow_none=False)
    githubApiUrl = fields.Url(required=True, allow_none=False)


def _run_information_serialization_disambiguation(base_object, parent_obj):
    if isinstance(base_object, LocalRunInformationSchema):
        return LocalRunInformationSchema()
    elif isinstance(base_object, GithubActionsRunInformation):
        return GithubActionsRunInformationSchema()

    raise TypeError(f"Could not detect type for {base_object.__class__.__name__}")


def _run_information_deserialization_disambiguation(object_dict, parent_object_dict):
    if object_dict.get("runInformationType") == RunBatchProvider.LOCAL_COMPUTER.name:
        return LocalRunInformationSchema()
    elif object_dict.get("runInformationType") == RunBatchProvider.GITHUB_ACTIONS.name:
        return GithubActionsRunInformationSchema()

    raise TypeError(f"Could not detect type for {object_dict.get('type')}")


class CreateFullRunSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    projectId = ID_FIELD
    runBatchIdentifier = fields.Nested(RunBatchIdentifierSchema, required=True)
    testSuites = fields.List(
        fields.Nested(TestSuiteForRunCreationSchema), required=True
    )
    branchName = fields.String(
        validate=[Length(min=1)], required=False, allow_none=True
    )

    runInformation = PolyField(
        serialization_schema_selector=_run_information_serialization_disambiguation,
        deserialization_schema_selector=_run_information_deserialization_disambiguation,
        required=True,
    )
