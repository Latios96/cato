from cato.domain.test_status import TestStatus
from cato_common.domain.compare_image_result import CompareImageResult


def test_map_from(object_mapper):
    result = object_mapper.from_dict(
        {
            "status": "SUCCESS",
            "message": "message",
            "reference_image_id": 1,
            "output_image_id": 2,
            "diff_image_id": 3,
        },
        CompareImageResult,
    )

    assert result == CompareImageResult(
        status=TestStatus.SUCCESS,
        message="message",
        reference_image_id=1,
        output_image_id=2,
        diff_image_id=3,
    )


def test_map_from_optional_data(object_mapper):
    result = object_mapper.from_dict(
        {
            "status": "SUCCESS",
            "reference_image_id": 1,
            "output_image_id": 2,
            "diff_image_id": 3,
        },
        CompareImageResult,
    )

    assert result == CompareImageResult(
        status=TestStatus.SUCCESS,
        message=None,
        reference_image_id=1,
        output_image_id=2,
        diff_image_id=3,
    )


def test_map_to(object_mapper):
    result = object_mapper.to_dict(
        CompareImageResult(
            status=TestStatus.SUCCESS,
            message="message",
            reference_image_id=1,
            output_image_id=2,
            diff_image_id=3,
        )
    )

    assert result == {
        "status": "SUCCESS",
        "message": "message",
        "reference_image_id": 1,
        "output_image_id": 2,
        "diff_image_id": 3,
    }
