from dataclasses import dataclass

from cato_common.domain.run_batch_provider import RunBatchProvider
from cato_common.domain.run_identifier import RunIdentifier
from cato_common.domain.run_name import RunName


@dataclass(frozen=True)
class RunBatchIdentifier:
    provider: RunBatchProvider
    run_name: RunName
    run_identifier: RunIdentifier
