import os
import sys

from cato_common.domain.run_batch_identifier import RunBatchIdentifier
from cato_common.domain.run_batch_provider import RunBatchProvider
from cato_common.domain.run_identifier import RunIdentifier
from cato_common.domain.run_name import RunName


class RunBatchIdentifierDetector:
    def __init__(self, environment=os.environ):
        self._environment = environment

    def detect(self) -> RunBatchIdentifier:
        if self._is_github_actions():
            return self._collect_github_actions()

        return self._local_computer()

    def _is_github_actions(self) -> bool:
        return self._environment.get("GITHUB_ACTION") is not None

    def _collect_github_actions(self) -> RunBatchIdentifier:
        job = RunName(self._environment["GITHUB_JOB"])

        run_id = self._environment["GITHUB_RUN_ID"]
        attempt = self._environment["GITHUB_RUN_ATTEMPT"]
        run_identifier = RunIdentifier(f"{run_id}-{attempt}")

        return RunBatchIdentifier(
            provider=RunBatchProvider.GITHUB_ACTIONS,
            run_name=job,
            run_identifier=run_identifier,
        )

    def _local_computer(self) -> RunBatchIdentifier:
        return RunBatchIdentifier(
            provider=RunBatchProvider.LOCAL_COMPUTER,
            run_name=_platform_to_run_name(),
            run_identifier=RunIdentifier.random(),
        )


def _platform_to_run_name() -> RunName:
    return {
        "win32": RunName("windows"),
        "linux": RunName("linux"),
        "darwin": RunName("mac-os"),
    }[sys.platform]
