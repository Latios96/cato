from cato.config.config_file_parser import JsonConfigParser
from cato.config.config_file_writer import ConfigFileWriter
from cato_server.domain.submission_info import SubmissionInfo
from cato_server.storage.sqlalchemy.sqlalchemy_submission_info_repository import (
    SqlAlchemySubmissionInfoRepository,
)


def test_save_submission_info(config_fixture, sessionmaker_fixture, run):
    repository = SqlAlchemySubmissionInfoRepository(
        sessionmaker_fixture, JsonConfigParser(), ConfigFileWriter()
    )
    submission_info = SubmissionInfo(
        id=0,
        config=config_fixture.CONFIG,
        run_id=run.id,
        resource_path="resource_path",
        executable="executable",
    )

    stored_info = repository.save(submission_info)

    submission_info.id = 1
    assert stored_info == submission_info


def test_find_by_id_should_return(config_fixture, sessionmaker_fixture, run):
    repository = SqlAlchemySubmissionInfoRepository(
        sessionmaker_fixture, JsonConfigParser(), ConfigFileWriter()
    )
    submission_info = SubmissionInfo(
        id=0,
        config=config_fixture.CONFIG,
        run_id=run.id,
        resource_path="resource_path",
        executable="executable",
    )
    stored_info = repository.save(submission_info)

    found_info = repository.find_by_id(stored_info.id)

    assert stored_info == found_info
