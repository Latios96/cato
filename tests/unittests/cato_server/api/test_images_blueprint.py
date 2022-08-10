import pytest

API_V_IMAGES = "/api/v1/images"
API_V_IMAGES_ASYNC = "/api/v1/images-async"


def test_upload_image(client_with_session, test_resource_provider):
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {"file": ("test_image_white.jpg", open(test_image, "rb"))}
    response = client_with_session.post(API_V_IMAGES, files=data)

    assert response.status_code == 201
    assert response.json() == {
        "channels": [{"fileId": 2, "id": 1, "imageId": 1, "name": "rgb"}],
        "id": 1,
        "name": "test_image_white.jpg",
        "originalFileId": 1,
        "width": 100,
        "height": 100,
    }


def test_upload_image_no_filename(client_with_session, test_resource_provider):
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {"file": ("", open(test_image, "rb"))}
    response = client_with_session.post(API_V_IMAGES, files=data)

    assert response.status_code == 400
    assert response.json() == {"file": "Filename can not be empty!"}


def test_get_image_not_found(client_with_session):
    response = client_with_session.get("/api/v1/images/42")

    assert response.status_code == 404


def test_get_image_found_image(client_with_session, test_resource_provider):
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {"file": ("test_image_white.jpg", open(test_image, "rb"))}
    response = client_with_session.post(API_V_IMAGES, files=data)
    image_id = response.json()["id"]

    response = client_with_session.get(f"/api/v1/images/{image_id}")

    assert response.status_code == 200
    assert response.json() == {
        "channels": [{"fileId": 2, "id": 1, "imageId": 1, "name": "rgb"}],
        "id": 1,
        "name": "test_image_white.jpg",
        "originalFileId": 1,
        "width": 100,
        "height": 100,
    }


def test_upload_unsupported_file(client_with_session, test_resource_provider):
    test_file = test_resource_provider.resource_by_name("unsupported-file.txt")
    data = {"file": ("test_file.txt", open(test_file, "rb"))}

    response = client_with_session.post(API_V_IMAGES, files=data)

    assert response.status_code == 400


def test_upload_async_image(
    client_with_session, test_resource_provider, app_and_config_fixture
):
    app, config = app_and_config_fixture
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {"file": ("test_image_white.jpg", open(test_image, "rb"))}
    response = client_with_session.post(API_V_IMAGES_ASYNC, files=data)

    assert response.status_code == 201
    response_json = response.json()
    assert len(response_json.pop("taskId")) == 36
    assert response_json == {
        "errorMessage_": None,
        "result_": {
            "image": {
                "channels": [{"fileId": 2, "id": 1, "imageId": 1, "name": "rgb"}],
                "height": 100,
                "id": 1,
                "name": "test_image_white.jpg",
                "originalFileId": 1,
                "width": 100,
            }
        },
        "state": "SUCCESS",
        "url": f"http://127.0.0.1:{config.port}/api/v1/result/{response.json()['taskId']}",
    }


def test_upload_image_async_no_filename(client_with_session, test_resource_provider):
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {"file": ("", open(test_image, "rb"))}
    response = client_with_session.post(API_V_IMAGES_ASYNC, files=data)

    assert response.status_code == 400
    assert response.json() == {"file": "Filename can not be empty!"}


def test_upload_async_unsupported_file(client_with_session, test_resource_provider):
    test_file = test_resource_provider.resource_by_name("unsupported-file.txt")
    data = {"file": ("test_file.txt", open(test_file, "rb"))}

    response = client_with_session.post(API_V_IMAGES_ASYNC, files=data)

    assert response.json()["state"] == "FAILURE"


def test_get_original_image_file_should_return_file(client_with_session, stored_image):
    response = client_with_session.get(
        f"/api/v1/images/original_file/{stored_image.id}"
    )

    assert response.status_code == 200
    assert len(response.content) == 87444


def test_get_original_image_file_should_return_404(client_with_session):
    response = client_with_session.get("/api/v1/images/original_file/42")

    assert response.status_code == 404
