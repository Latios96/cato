from sqlalchemy.orm import sessionmaker

from cato.storage.sqlalchemy.sqlalchemy_deduplicating_file_storage import (
    SqlAlchemyDeduplicatingFileStorage,
)
from cato.storage.sqlalchemy.sqlalchemy_project_repository import (
    SqlAlchemyProjectRepository,
)
from cato.storage.sqlalchemy.sqlalchemy_run_repository import SqlAlchemyRunRepository
from cato.storage.sqlalchemy.sqlalchemy_suite_result_repository import (
    SqlAlchemySuiteResultRepository,
)
from cato.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)
from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.bindings_factory import BindingsFactory
from cato_server.configuration.storage_configuration import StorageConfiguration


# postgres
# in memory
# mock
def test_create_storage_bindings_for_postgres():
    configuration = AppConfiguration(
        port=5000,
        storage_configuration=StorageConfiguration(
            database_url="postgresql+psycopg2://username:password@localhost:5432/db_name",
            file_storage_url="some_path",
        ),
    )
    bindings_factory = BindingsFactory(configuration)

    storage_bindings = bindings_factory.create_storage_bindings()

    assert storage_bindings.project_repository_binding == SqlAlchemyProjectRepository
    assert storage_bindings.run_repository_binding == SqlAlchemyRunRepository
    assert (
        storage_bindings.suite_result_repository_binding
        == SqlAlchemySuiteResultRepository
    )
    assert (
        storage_bindings.test_result_repository_binding
        == SqlAlchemyTestResultRepository
    )
    assert storage_bindings.file_storage_binding == SqlAlchemyDeduplicatingFileStorage
    assert storage_bindings.root_path_binding == "some_path"
    assert isinstance(storage_bindings.session_maker_binding, sessionmaker)
