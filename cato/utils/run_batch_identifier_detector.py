import sys

from cato_common.domain.run_batch_identifier import RunBatchIdentifier
from cato_common.domain.run_batch_provider import RunBatchProvider
from cato_common.domain.run_identifier import RunIdentifier
from cato_common.domain.run_name import RunName


class RunBatchIdentifierDetector:
    def detect(self) -> RunBatchIdentifier:
        return self._local_computer()

    def _local_computer(self):
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
