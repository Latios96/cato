from cato_server.domain.comparison_method import ComparisonMethod
from cato_server.domain.comparison_settings import ComparisonSettings


def test_upload_images_for_comparison_success(
    client, test_resource_provider, object_mapper
):
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {
        "reference_image": ("reference_image.png", open(test_image, "rb")),
        "output_image": ("output_image.png", open(test_image, "rb")),
    }
    response = client.post(
        "/api/v1/compare_image",
        files=data,
        data={
            "comparison_settings": object_mapper.to_json(
                ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1)
            )
        },
    )

    assert response.json() == {
        "message": None,
        "output_image_id": 1,
        "reference_image_id": 2,
        "status": "SUCCESS",
    }
    assert response.status_code == 201


def test_upload_images_should_fail_no_parsable_comparison_settings(
    client, test_resource_provider, object_mapper
):
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {
        "reference_image": ("reference_image.png", open(test_image, "rb")),
        "output_image": ("output_image.png", open(test_image, "rb")),
    }
    response = client.post(
        "/api/v1/compare_image",
        files=data,
        data={"comparison_settings": "test"},
    )

    assert response.json() == {
        "comparison_settings": "Error when parsing comparison settings: Expecting "
        "value: line 1 column 1 (char 0)"
    }
    assert response.status_code == 400


def test_upload_images_should_fail_no_reference_image(
    client, test_resource_provider, object_mapper
):
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {
        "output_image": ("output_image.png", open(test_image, "rb")),
    }
    response = client.post(
        "/api/v1/compare_image",
        files=data,
        data={
            "comparison_settings": object_mapper.to_json(
                ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1)
            )
        },
    )

    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "reference_image"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
    assert response.status_code == 422


def test_upload_should_fail_with_non_image_data(
    client, test_resource_provider, object_mapper
):
    test_image = test_resource_provider.resource_by_name("unsupported-file.txt")
    data = {
        "reference_image": ("reference_image.png", open(test_image, "rb")),
        "output_image": ("output_image.png", open(test_image, "rb")),
    }
    response = client.post(
        "/api/v1/compare_image",
        files=data,
        data={
            "comparison_settings": object_mapper.to_json(
                ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1)
            )
        },
    )

    assert response.json()["error"].startswith(
        "Error when comparing images: Exit code f1 when running command"
    )
    assert response.status_code == 400
