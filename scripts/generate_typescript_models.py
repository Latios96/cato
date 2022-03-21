from pathlib import Path

from py_typescript_generator import TypeGenerationPipelineBuilder

from cato_common.domain.auth.email import Email
from cato_common.domain.auth.username import Username
from cato_common.domain.branch_name import BranchName
from cato_common.domain.can_be_edited import CanBeEdited
from cato_common.domain.project import Project
from cato_common.domain.test_failure_reason import TestFailureReason
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.dtos.create_full_run_dto import CreateFullRunDto
from cato_common.dtos.run_summary_dto import RunSummaryDto
from cato_common.dtos.suite_result_dto import SuiteResultDto
from cato_common.dtos.test_result_dto import TestResultDto
from cato_common.dtos.test_result_short_summary_dto import TestResultShortSummaryDto
from cato_server.api.dtos.test_edit_count import TestEditCount
from cato_server.domain.auth.auth_user import AuthUser
from cato_server.storage.abstract.status_filter import StatusFilter

if __name__ == "__main__":
    TypeGenerationPipelineBuilder().for_types(
        [
            Project,
            CanBeEdited,
            TestEditCount,
            StatusFilter,
            TestFailureReason,
            TestResultShortSummaryDto,
            SuiteResultDto,
            TestResultDto,
            RunSummaryDto,
            CreateFullRunDto,
            AuthUser,
        ]
    ).with_type_overrides(
        {TestIdentifier: str, BranchName: str, Username: str, Email: str}
    ).to_file(
        Path(__file__).parent.parent
        / "frontend"
        / "src"
        / "catoapimodels"
        / "catoapimodels.ts"
    ).convert_field_names_to_camel_case().build().run()
