API_V_IMAGES = "/api/v1/images"


def test_upload_image(client, test_resource_provider):
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {"file": ("test_image_white.jpg", open(test_image, "rb"))}
    response = client.post(API_V_IMAGES, files=data)

    assert response.status_code == 201
    assert response.json() == {
        "channels": [{"file_id": 2, "id": 1, "image_id": 1, "name": "rgb"}],
        "id": 1,
        "name": "test_image_white.jpg",
        "original_file_id": 1,
        "width": 100,
        "height": 100,
    }


def test_upload_image_no_filename(client, test_resource_provider):
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {"file": ("", open(test_image, "rb"))}
    response = client.post(API_V_IMAGES, files=data)

    assert response.status_code == 400
    assert response.json() == {"file": "Filename can not be empty!"}


def test_get_image_not_found(client):
    response = client.get("/api/v1/images/42")

    assert response.status_code == 404


def test_get_image_found_image(client, test_resource_provider):
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {"file": ("test_image_white.jpg", open(test_image, "rb"))}
    response = client.post(API_V_IMAGES, files=data)
    image_id = response.json()["id"]

    response = client.get(f"/api/v1/images/{image_id}")

    assert response.status_code == 200
    assert response.json() == {
        "channels": [{"file_id": 2, "id": 1, "image_id": 1, "name": "rgb"}],
        "id": 1,
        "name": "test_image_white.jpg",
        "original_file_id": 1,
        "width": 100,
        "height": 100,
    }


def test_upload_unsupported_file(client, test_resource_provider):
    test_file = test_resource_provider.resource_by_name("unsupported-file.txt")
    data = {"file": ("test_file.txt", open(test_file, "rb"))}

    response = client.post(API_V_IMAGES, files=data)

    assert response.status_code == 400


def test_get_original_image_file_should_return_file(client, stored_image):
    response = client.get(f"/api/v1/images/original_file/{stored_image.id}")

    assert response.status_code == 200
    assert len(response.content) == 87444


def test_get_original_image_file_should_return_404(client):
    response = client.get("/api/v1/images/original_file/42")

    assert response.status_code == 404
