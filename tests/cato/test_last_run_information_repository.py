import os

from cato.file_system_abstractions.last_run_information_repository import (
    CatoLastRunInformationRepository,
    LastRunInformation,
)


def test_should_write_and_read_back(tmp_path):
    repository = CatoLastRunInformationRepository(str(tmp_path))
    last_run_info = LastRunInformation(last_run_id=2)

    repository.write_last_run_information(last_run_info)
    result = repository.read_last_run_information()

    assert os.path.exists(repository._last_run_information_path())
    assert result == last_run_info


def test_should_overwrite(tmp_path):
    repository = CatoLastRunInformationRepository(str(tmp_path))

    repository.write_last_run_information(LastRunInformation(last_run_id=2))
    repository.write_last_run_information(LastRunInformation(last_run_id=3))

    result = repository.read_last_run_information()
    assert os.path.exists(repository._last_run_information_path())
    assert result == LastRunInformation(last_run_id=3)


def test_should_return_none(tmp_path):
    repository = CatoLastRunInformationRepository(str(tmp_path))

    result = repository.read_last_run_information()
    assert not result
