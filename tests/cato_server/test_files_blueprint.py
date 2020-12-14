import io

API_V_FILES = "/api/v1/files"


def test_upload_file(client):
    data = {"file": (io.BytesIO(b"some initial text data"), "my_file_name")}
    response = client.post(API_V_FILES, data=data)

    assert response.status_code == 201
    assert response.get_json() == {
        "hash": "43cb15ad0b6b6a956dfb128d0dd4d1fc93462968bdbf7a285579eda534772514",
        "id": 1,
        "name": "my_file_name",
        "value_counter": 0,
    }


def test_upload_file_no_filename(client):
    data = {"file": (io.BytesIO(b"some initial text data"), "")}
    response = client.post(API_V_FILES, data=data)

    assert response.status_code == 400
    assert response.get_json() == {"file": "Filename can not be empty!"}


def test_upload_file_needs_conversion(client, test_resource_provider):
    test_exr = test_resource_provider.resource_by_name("test.exr")
    data = {"file": (open(test_exr, "rb"), "test.exr")}
    response = client.post(API_V_FILES, data=data)

    assert response.status_code == 201
    assert response.get_json() == {
        "hash": "505cc9e0719a4f15a36eaa6df776bea0cc065b32d198be6002a79a03823b4d9e",
        "id": 1,
        "name": "test.png",
        "value_counter": 0,
    }


def test_serve_file(client):
    data = {"file": (io.BytesIO(b"some initial text data"), "my_file_name")}
    f = client.post(API_V_FILES, data=data).get_json()

    response = client.get(f"/api/v1/files/{f['id']}")

    assert response.status_code == 200
    assert response.data == b"some initial text data"
