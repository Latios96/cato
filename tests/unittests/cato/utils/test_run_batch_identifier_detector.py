from unittest import mock

import pytest

from cato.utils.run_batch_identifier_detector import (
    RunBatchIdentifierDetector,
    _platform_to_run_name,
)
from cato_common.domain.run_batch_identifier import RunBatchIdentifier
from cato_common.domain.run_batch_provider import RunBatchProvider
from cato_common.domain.run_identifier import RunIdentifier


@pytest.fixture
def test_context():
    with mock.patch(
        "cato_common.domain.run_identifier.RunIdentifier.random"
    ) as mock_generate_random:
        mock_generate_random.return_value = RunIdentifier(
            "98d5712b-816d-484d-a65d-3c6b75a0067d"
        )
        yield


def test_detect_local_computer(test_context):
    detector = RunBatchIdentifierDetector()

    run_batch_identifier = detector.detect()

    assert run_batch_identifier == RunBatchIdentifier(
        provider=RunBatchProvider.LOCAL_COMPUTER,
        run_name=_platform_to_run_name(),
        run_identifier=RunIdentifier("98d5712b-816d-484d-a65d-3c6b75a0067d"),
    )
