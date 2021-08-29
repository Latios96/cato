from dataclasses import dataclass

from cato_server.storage.abstract.status_filter import StatusFilter


@dataclass
class SuiteResultFilterOptions:
    status: StatusFilter
