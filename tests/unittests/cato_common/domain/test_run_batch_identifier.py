from cato_common.domain.run_batch_identifier import RunBatchIdentifier
from cato_common.domain.run_batch_provider import RunBatchProvider
from cato_common.domain.run_identifier import RunIdentifier
from cato_common.domain.run_name import RunName


def test_should_return_copy_with_different_provider():
    run_batch_identifier = RunBatchIdentifier(
        provider=RunBatchProvider.LOCAL_COMPUTER,
        run_name=RunName("mac-os"),
        run_identifier=RunIdentifier("3046812908-1"),
    )

    new_run_batch_identifier = run_batch_identifier.copy(
        provider=RunBatchProvider.GITHUB_ACTIONS
    )

    assert new_run_batch_identifier == RunBatchIdentifier(
        provider=RunBatchProvider.GITHUB_ACTIONS,
        run_name=RunName("mac-os"),
        run_identifier=RunIdentifier("3046812908-1"),
    )


def test_should_return_copy_with_run_name():
    run_batch_identifier = RunBatchIdentifier(
        provider=RunBatchProvider.LOCAL_COMPUTER,
        run_name=RunName("mac-os"),
        run_identifier=RunIdentifier("3046812908-1"),
    )

    new_run_batch_identifier = run_batch_identifier.copy(run_name=RunName("linux"))

    assert new_run_batch_identifier == RunBatchIdentifier(
        provider=RunBatchProvider.LOCAL_COMPUTER,
        run_name=RunName("linux"),
        run_identifier=RunIdentifier("3046812908-1"),
    )


def test_should_return_copy_with_run_identifier():
    run_batch_identifier = RunBatchIdentifier(
        provider=RunBatchProvider.LOCAL_COMPUTER,
        run_name=RunName("mac-os"),
        run_identifier=RunIdentifier("3046812908-1"),
    )

    new_run_batch_identifier = run_batch_identifier.copy(
        run_identifier=RunIdentifier("3046812908-2")
    )

    assert new_run_batch_identifier == RunBatchIdentifier(
        provider=RunBatchProvider.LOCAL_COMPUTER,
        run_name=RunName("mac-os"),
        run_identifier=RunIdentifier("3046812908-2"),
    )
