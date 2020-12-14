import io
import os

import pytest

API_V_IMAGES = "/api/v1/images"


def test_upload_file(client, test_resource_provider):
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {"file": (open(test_image, "rb"), "test_image_white.jpg")}
    response = client.post(API_V_IMAGES, data=data)

    assert response.status_code == 201
    assert response.get_json() == {
        "channels": [{"file_id": 2, "id": 1, "image_id": 1, "name": "rgb"}],
        "id": 1,
        "name": "test_image_white.jpg",
        "original_file_id": 1,
    }


def test_upload_file_no_filename(client, test_resource_provider):
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {"file": (open(test_image, "rb"), "")}
    response = client.post(API_V_IMAGES, data=data)

    assert response.status_code == 400
    assert response.get_json() == {"file": "Filename can not be empty!"}
