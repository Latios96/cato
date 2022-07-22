import pytest
import requests
from tenacity import stop_after_attempt, wait_fixed, retry

from tests.integrationtests.utils import tenacity_before_print


@pytest.fixture
def celery_binding(celery_app):
    return celery_app


@pytest.fixture
def live_server_with_celery(live_server, celery_app, celery_worker):
    celery_worker.reload()
    return live_server


@pytest.fixture
def authenticated_requests_session(http_session_cookie, crsf_token):
    session_cookie_name, session_cookie_value = http_session_cookie

    session = requests.Session()
    session.cookies.set(session_cookie_name, session_cookie_value)
    session.cookies["XSRF-TOKEN"] = crsf_token
    session.headers["X-XSRF-TOKEN"] = crsf_token

    return session


def test_thumbnail_should_be_created_async_after_finising_test(
    live_server_with_celery, authenticated_requests_session, test_result, stored_image
):
    url = live_server_with_celery.server_url() + "/api/v1/test_results/finish"
    data = {
        "id": test_result.id,
        "status": "SUCCESS",
        "seconds": 3,
        "message": "this is my finishing message",
        "imageOutput": stored_image.id,
        "referenceImage": stored_image.id,
        "errorValue": 1,
    }

    response = authenticated_requests_session.post(url, json=data)
    assert response.status_code == 200

    @retry(
        stop=stop_after_attempt(20), wait=wait_fixed(1), before=tenacity_before_print()
    )
    def wait_for_thumbnail_to_appear():
        url = (
            live_server_with_celery.server_url()
            + f"/api/v1/test_results/{test_result.id}"
        )
        rv = authenticated_requests_session.get(url)

        assert rv.status_code == 200
        assert rv.json()["thumbnailFileId"] != None

    wait_for_thumbnail_to_appear()
