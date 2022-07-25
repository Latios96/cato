from sqlalchemy.orm import sessionmaker

from cato_common.domain.project import Project
from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.app_configuration_defaults import (
    AppConfigurationDefaults,
)
from cato_server.configuration.bindings_factory import (
    BindingsFactory,
)
from cato_server.configuration.parts.celery_configuration import CeleryConfiguration
from cato_server.configuration.parts.logging_configuration import LoggingConfiguration
from cato_server.configuration.oidc_config import OidcConfiguration
from cato_server.configuration.parts.oiio_configuration import OiioConfiguration
from cato_server.configuration.parts.scheduler_configuration import (
    SchedulerConfiguration,
    DeadlineSchedulerConfiguration,
)
from cato_server.configuration.parts.secrets_configuration import SecretsConfiguration
from cato_server.configuration.parts.sentry_configuration import SentryConfiguration
from cato_server.configuration.parts.session_configuration import SessionConfiguration
from cato_server.configuration.parts.storage_configuration import StorageConfiguration
from cato_server.domain.auth.secret_str import SecretStr
from cato_server.storage.sqlalchemy.sqlalchemy_deduplicating_file_storage import (
    SqlAlchemyDeduplicatingFileStorage,
)
from cato_server.storage.sqlalchemy.sqlalchemy_project_repository import (
    SqlAlchemyProjectRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_run_repository import (
    SqlAlchemyRunRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_suite_result_repository import (
    SqlAlchemySuiteResultRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)


def test_create_storage_bindings_for_postgres():
    configuration = AppConfiguration(
        port=5000,
        debug=True,
        secrets_configuration=SecretsConfiguration(
            sessions_secret=SecretStr("SESSIONS_SECRET"),
            csrf_secret=SecretStr("CSRF_SECRET"),
            api_tokens_secret=SecretStr("API_TOKENS_SECRET"),
        ),
        hostname="localhost",
        public_url="http://127.0.0.1",
        storage_configuration=StorageConfiguration(
            database_url="postgresql+psycopg2://username:password@localhost:5432/db_name",
            file_storage_url="some_path",
        ),
        logging_configuration=LoggingConfiguration(
            log_file_path=AppConfigurationDefaults.LOG_FILE_PATH_DEFAULT,
            use_file_handler=AppConfigurationDefaults.USE_FILE_HANDLER_DEFAULT,
            max_bytes=AppConfigurationDefaults.MAX_BYTES_DEFAULT,
            backup_count=AppConfigurationDefaults.BACKUP_COUNT_DEFAULT,
        ),
        scheduler_configuration=SchedulerConfiguration(),
        sentry_configuration=SentryConfiguration.default(),
        session_configuration=SessionConfiguration.default(),
        oidc_configuration=OidcConfiguration(
            client_id="client-id",
            client_secret=SecretStr("secret"),
            well_known_url="http://somewhere",
        ),
        celery_configuration=CeleryConfiguration(
            broker_url="pyamqp://guest@localhost//"
        ),
        oiio_configuration=OiioConfiguration(thread_count=1),
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


def test_create_storage_bindings_using_sqlite_in_memory():
    configuration = AppConfiguration(
        port=5000,
        debug=True,
        secrets_configuration=SecretsConfiguration(
            sessions_secret=SecretStr("SESSIONS_SECRET"),
            csrf_secret=SecretStr("CSRF_SECRET"),
            api_tokens_secret=SecretStr("API_TOKENS_SECRET"),
        ),
        hostname="localhost",
        public_url="http://127.0.0.1",
        storage_configuration=StorageConfiguration(
            database_url="sqlite:///:memory:",
            file_storage_url="some_path",
        ),
        logging_configuration=LoggingConfiguration(
            log_file_path=AppConfigurationDefaults.LOG_FILE_PATH_DEFAULT,
            use_file_handler=AppConfigurationDefaults.USE_FILE_HANDLER_DEFAULT,
            max_bytes=AppConfigurationDefaults.MAX_BYTES_DEFAULT,
            backup_count=AppConfigurationDefaults.BACKUP_COUNT_DEFAULT,
        ),
        scheduler_configuration=SchedulerConfiguration(),
        sentry_configuration=SentryConfiguration.default(),
        session_configuration=SessionConfiguration.default(),
        oidc_configuration=OidcConfiguration(
            client_id="client-id",
            client_secret=SecretStr("secret"),
            well_known_url="http://somewhere",
        ),
        celery_configuration=CeleryConfiguration(
            broker_url="pyamqp://guest@localhost//"
        ),
        oiio_configuration=OiioConfiguration(thread_count=1),
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

    assert (
        SqlAlchemyProjectRepository(storage_bindings.session_maker_binding)
        .save(Project(id=0, name="test"))
        .id
        == 1
    )


def test_create_scheduler_bindings_no_scheduler():
    config = AppConfiguration(
        port=5000,
        debug=True,
        secrets_configuration=SecretsConfiguration(
            sessions_secret=SecretStr("SESSIONS_SECRET"),
            csrf_secret=SecretStr("CSRF_SECRET"),
            api_tokens_secret=SecretStr("API_TOKENS_SECRET"),
        ),
        hostname="localhost",
        public_url="http://127.0.0.1",
        storage_configuration=StorageConfiguration(
            database_url="sqlite:///:memory:",
            file_storage_url="some_path",
        ),
        logging_configuration=LoggingConfiguration(
            log_file_path=AppConfigurationDefaults.LOG_FILE_PATH_DEFAULT,
            use_file_handler=AppConfigurationDefaults.USE_FILE_HANDLER_DEFAULT,
            max_bytes=AppConfigurationDefaults.MAX_BYTES_DEFAULT,
            backup_count=AppConfigurationDefaults.BACKUP_COUNT_DEFAULT,
        ),
        scheduler_configuration=SchedulerConfiguration(),
        sentry_configuration=SentryConfiguration.default(),
        session_configuration=SessionConfiguration.default(),
        oidc_configuration=OidcConfiguration(
            client_id="client-id",
            client_secret=SecretStr("secret"),
            well_known_url="http://somewhere",
        ),
        celery_configuration=CeleryConfiguration(
            broker_url="pyamqp://guest@localhost//"
        ),
        oiio_configuration=OiioConfiguration(thread_count=1),
    )
    bindings_factory = BindingsFactory(config)

    scheduler_bindings = bindings_factory.create_scheduler_bindings()

    assert scheduler_bindings.scheduler_submitter_binding.empty()


CONFIG_FOR_DEADLINE_TESTING = AppConfiguration(
    port=5000,
    debug=True,
    secrets_configuration=SecretsConfiguration(
        sessions_secret=SecretStr("SESSIONS_SECRET"),
        csrf_secret=SecretStr("CSRF_SECRET"),
        api_tokens_secret=SecretStr("API_TOKENS_SECRET"),
    ),
    hostname="localhost",
    public_url="http://127.0.0.1",
    storage_configuration=StorageConfiguration(
        database_url="sqlite:///:memory:",
        file_storage_url="some_path",
    ),
    logging_configuration=LoggingConfiguration(
        log_file_path=AppConfigurationDefaults.LOG_FILE_PATH_DEFAULT,
        use_file_handler=AppConfigurationDefaults.USE_FILE_HANDLER_DEFAULT,
        max_bytes=AppConfigurationDefaults.MAX_BYTES_DEFAULT,
        backup_count=AppConfigurationDefaults.BACKUP_COUNT_DEFAULT,
    ),
    scheduler_configuration=DeadlineSchedulerConfiguration("test"),
    sentry_configuration=SentryConfiguration.default(),
    session_configuration=SessionConfiguration.default(),
    oidc_configuration=OidcConfiguration(
        client_id="client-id",
        client_secret=SecretStr("secret"),
        well_known_url="http://somewhere",
    ),
    celery_configuration=CeleryConfiguration(broker_url="test"),
    oiio_configuration=OiioConfiguration(thread_count=1),
)


def test_create_scheduler_bindings_with_deadline():
    bindings_factory = BindingsFactory(CONFIG_FOR_DEADLINE_TESTING)
    bindings_factory._deadline_is_available = lambda x: True

    scheduler_bindings = bindings_factory.create_scheduler_bindings()

    assert scheduler_bindings.scheduler_submitter_binding.is_available()


def test_create_scheduler_bindings_deadline_not_available():
    bindings_factory = BindingsFactory(CONFIG_FOR_DEADLINE_TESTING)
    bindings_factory._deadline_is_available = lambda x: True

    scheduler_bindings = bindings_factory.create_scheduler_bindings()

    assert scheduler_bindings.scheduler_submitter_binding.empty()
