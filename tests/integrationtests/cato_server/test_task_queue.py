from tenacity import stop_after_attempt, wait_fixed, retry

from tests.integrationtests.cato_server import testcontainers_test, celery_test
from tests.integrationtests.utils import tenacity_before_print


@celery_test
@testcontainers_test
def test_thumbnail_should_be_created_async_after_finising_test(
    live_server, authenticated_requests_session, test_result, stored_image
):
    url = live_server.server_url() + "/api/v1/test_results/finish"
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
        stop=stop_after_attempt(20), wait=wait_fixed(2), before=tenacity_before_print()
    )
    def wait_for_thumbnail_to_appear():
        url = live_server.server_url() + f"/api/v1/test_results/{test_result.id}"
        rv = authenticated_requests_session.get(url)

        assert rv.status_code == 200
        assert rv.json()["thumbnailFileId"] != None

    wait_for_thumbnail_to_appear()
