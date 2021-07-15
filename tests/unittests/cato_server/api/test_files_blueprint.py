import io

API_V_FILES = "/api/v1/files"


def test_upload_file(client):
    data = {"file": ("my_file_name", io.BytesIO(b"some initial text data"))}
    response = client.post(API_V_FILES, files=data)

    assert response.status_code == 201
    assert response.json() == {
        "hash": "43cb15ad0b6b6a956dfb128d0dd4d1fc93462968bdbf7a285579eda534772514",
        "id": 1,
        "name": "my_file_name",
        "value_counter": 0,
    }


def test_upload_file_no_filename(client):
    data = {"file": ("", io.BytesIO(b"some initial text data"))}
    response = client.post(API_V_FILES, files=data)

    assert response.status_code == 400
    assert response.json() == {"file": "Filename can not be empty!"}


def test_serve_file(client):
    data = {"file": ("my_file_name", io.BytesIO(b"some initial text data"))}
    f = client.post(API_V_FILES, files=data).json()

    response = client.get(f"/api/v1/files/{f['id']}")

    assert response.status_code == 200
    assert response.content == b"some initial text data"
