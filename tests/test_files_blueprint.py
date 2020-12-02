import io

import pytest

API_V_FILES = "/api/v1/files"


def test_upload_file(client):
    data = {"file": (io.BytesIO(b"some initial text data"), "my_file_name")}
    response = client.post(API_V_FILES, data=data)

    assert response.status_code == 201
    assert response.get_json() == {
        "hash": "43cb15ad0b6b6a956dfb128d0dd4d1fc93462968bdbf7a285579eda534772514",
        "id": 1,
        "name": "my_file_name",
    }


def test_upload_file_no_filename(client):
    data = {"file": (io.BytesIO(b"some initial text data"), "")}
    response = client.post(API_V_FILES, data=data)

    assert response.status_code == 400
    assert response.get_json() == {"file": "Filename can not be empty!"}
