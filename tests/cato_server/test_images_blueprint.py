import io
import os

import pytest

API_V_IMAGES = "/api/v1/images"


def test_upload_image(client, test_resource_provider):
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {"file": (open(test_image, "rb"), "test_image_white.jpg")}
    response = client.post(API_V_IMAGES, data=data)

    assert response.status_code == 201
    assert response.get_json() == {
        "channels": [{"file_id": 2, "id": 1, "image_id": 1, "name": "rgb"}],
        "id": 1,
        "name": "test_image_white.jpg",
        "original_file_id": 1,
        "width": 100,
        "height": 100,
    }


def test_upload_image_no_filename(client, test_resource_provider):
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {"file": (open(test_image, "rb"), "")}
    response = client.post(API_V_IMAGES, data=data)

    assert response.status_code == 400
    assert response.get_json() == {"file": "Filename can not be empty!"}


def test_get_image_not_found(client):
    response = client.get("/api/v1/images/42")

    assert response.status_code == 404


def test_get_image_found_image(client, test_resource_provider):
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {"file": (open(test_image, "rb"), "test_image_white.jpg")}
    response = client.post(API_V_IMAGES, data=data)
    image_id = response.get_json()["id"]

    response = client.get(f"/api/v1/images/{image_id}")

    assert response.status_code == 200
    assert response.get_json() == {
        "channels": [{"file_id": 2, "id": 1, "image_id": 1, "name": "rgb"}],
        "id": 1,
        "name": "test_image_white.jpg",
        "original_file_id": 1,
        "width": 100,
        "height": 100,
    }
