import pytest

from cato_common.domain.image import Image, ImageChannel
from tests.integrationtests.cato_server import testcontainers_test, celery_test
from tests.integrationtests.postgres_testcontainer import PgContainer


@pytest.fixture
def celery_binding(celery_app):
    return celery_app


@pytest.fixture
def db_connection_string():
    with PgContainer() as postgres_container:
        yield postgres_container.get_connection_url()


@pytest.fixture
def cato_api_client_with_celery(cato_api_client, celery_worker):
    celery_worker.reload()
    yield cato_api_client


@celery_test
@testcontainers_test
def test_upload_image_async(cato_api_client_with_celery, test_resource_provider):
    path = test_resource_provider.resource_by_name("test.exr")

    f = cato_api_client_with_celery.upload_image_async(path)

    assert f == Image(
        id=1,
        name="test.exr",
        original_file_id=1,
        channels=[ImageChannel(id=1, image_id=1, name="rgb", file_id=2)],
        width=2048,
        height=1556,
    )
