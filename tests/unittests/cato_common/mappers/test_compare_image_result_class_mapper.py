from cato_common.domain.result_status import ResultStatus
from cato_common.domain.compare_image_result import CompareImageResult


def test_map_from(object_mapper):
    result = object_mapper.from_dict(
        {
            "status": "SUCCESS",
            "message": "message",
            "referenceImageId": 1,
            "outputImageId": 2,
            "diffImageId": 3,
            "error": 4,
        },
        CompareImageResult,
    )

    assert result == CompareImageResult(
        status=ResultStatus.SUCCESS,
        message="message",
        reference_image_id=1,
        output_image_id=2,
        diff_image_id=3,
        error=4,
    )


def test_map_from_optional_data(object_mapper):
    result = object_mapper.from_dict(
        {
            "status": "SUCCESS",
            "referenceImageId": 1,
            "outputImageId": 2,
            "diffImageId": 3,
            "error": 4,
        },
        CompareImageResult,
    )

    assert result == CompareImageResult(
        status=ResultStatus.SUCCESS,
        message=None,
        reference_image_id=1,
        output_image_id=2,
        diff_image_id=3,
        error=4,
    )


def test_map_to(object_mapper):
    result = object_mapper.to_dict(
        CompareImageResult(
            status=ResultStatus.SUCCESS,
            message="message",
            reference_image_id=1,
            output_image_id=2,
            diff_image_id=3,
            error=4,
        )
    )

    assert result == {
        "status": "SUCCESS",
        "message": "message",
        "referenceImageId": 1,
        "outputImageId": 2,
        "diffImageId": 3,
        "error": 4,
    }
