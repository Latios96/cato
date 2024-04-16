from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.comparison_settings import ComparisonSettings


def test_upload_images_for_comparison_success(
    client_with_session, test_resource_provider, object_mapper
):
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {
        "reference_image": ("reference_image.png", open(test_image, "rb")),
        "output_image": ("output_image.png", open(test_image, "rb")),
    }
    response = client_with_session.post(
        "/api/v1/compare_image",
        files=data,
        data={
            "comparison_settings": object_mapper.to_json(
                ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1)
            )
        },
    )

    assert response.json()["result_"] == {
        "message": None,
        "outputImageId": 1,
        "referenceImageId": 2,
        "diffImageId": 3,
        "status": "SUCCESS",
        "error": 1.0,
    }
    assert response.status_code == 201


def test_upload_images_should_fail_no_parsable_comparison_settings(
    client_with_session, test_resource_provider, object_mapper
):
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {
        "reference_image": ("reference_image.png", open(test_image, "rb")),
        "output_image": ("output_image.png", open(test_image, "rb")),
    }
    response = client_with_session.post(
        "/api/v1/compare_image",
        files=data,
        data={"comparison_settings": "test"},
    )

    assert response.json() == {
        "comparisonSettings": "Error when parsing comparison settings: Expecting "
        "value: line 1 column 1 (char 0)"
    }
    assert response.status_code == 400


def test_upload_images_should_fail_no_reference_image(
    client_with_session, test_resource_provider, object_mapper
):
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {
        "output_image": ("output_image.png", open(test_image, "rb")),
    }
    response = client_with_session.post(
        "/api/v1/compare_image",
        files=data,
        data={
            "comparison_settings": object_mapper.to_json(
                ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1)
            )
        },
    )

    assert response.status_code == 422


def test_upload_should_fail_with_non_image_data(
    client_with_session, test_resource_provider, object_mapper
):
    test_image = test_resource_provider.resource_by_name("unsupported-file.txt")
    data = {
        "reference_image": ("reference_image.png", open(test_image, "rb")),
        "output_image": ("output_image.png", open(test_image, "rb")),
    }
    response = client_with_session.post(
        "/api/v1/compare_image",
        files=data,
        data={
            "comparison_settings": object_mapper.to_json(
                ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1)
            )
        },
    )

    assert response.json()["errorMessage_"].startswith(
        "cato_server.images.oiio_command_executor.NotAnImageException"
    )
