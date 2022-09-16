from dataclasses import dataclass
from typing import Optional

from cato_common.domain.run_batch_provider import RunBatchProvider
from cato_common.domain.run_identifier import RunIdentifier
from cato_common.domain.run_name import RunName


@dataclass(frozen=True)
class RunBatchIdentifier:
    provider: RunBatchProvider
    run_name: RunName
    run_identifier: RunIdentifier

    def copy(
        self,
        provider=None,
        run_name=None,
        run_identifier=None,
    ):
        # type: (Optional[RunBatchProvider],Optional[RunName],Optional[RunIdentifier])->RunBatchIdentifier
        if not provider:
            provider = self.provider
        if not run_name:
            run_name = self.run_name
        if not run_identifier:
            run_identifier = self.run_identifier
        return RunBatchIdentifier(provider, run_name, run_identifier)
