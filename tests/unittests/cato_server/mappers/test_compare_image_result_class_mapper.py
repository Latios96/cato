from cato.domain.test_status import TestStatus
from cato_server.mappers.internal.compare_image_result_class_mapper import (
    CompareImageResultClassMapper,
)
from cato_server.usecases.compare_image import CompareImageResult


def test_map_from():
    mapper = CompareImageResultClassMapper()

    result = mapper.map_from_dict(
        {
            "status": "SUCCESS",
            "message": "message",
            "reference_image_id": 1,
            "output_image_id": 2,
            "diff_image_id": 3,
        }
    )

    assert result == CompareImageResult(
        status=TestStatus.SUCCESS,
        message="message",
        reference_image_id=1,
        output_image_id=2,
        diff_image_id=3,
    )


def test_map_from_optional_data():
    mapper = CompareImageResultClassMapper()

    result = mapper.map_from_dict(
        {
            "status": "SUCCESS",
            "reference_image_id": 1,
            "output_image_id": 2,
            "diff_image_id": 3,
        }
    )

    assert result == CompareImageResult(
        status=TestStatus.SUCCESS,
        message=None,
        reference_image_id=1,
        output_image_id=2,
        diff_image_id=3,
    )


def test_map_to():
    mapper = CompareImageResultClassMapper()

    result = mapper.map_to_dict(
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
