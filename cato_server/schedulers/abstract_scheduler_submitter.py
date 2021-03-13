import logging

from cato_server.schedulers.submission_info import SubmissionInfo

logger = logging.getLogger(__name__)


class AbstractSchedulerSubmitter:
    def submit_tests(self, submission_info: SubmissionInfo):
        raise NotImplementedError()
