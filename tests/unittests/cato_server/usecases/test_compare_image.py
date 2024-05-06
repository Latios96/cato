from io import BytesIO

import pytest

from cato_common.domain.result_status import ResultStatus
from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.comparison_result import ComparisonResult
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.file import File
from cato_common.domain.image import Image, ImageTranscodingState
from cato_common.images.image_comparators.ssim_image_comparator import (
    SsimImageComparator,
)
from cato_server.images.store_image import StoreImage
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.usecases.compare_image import CompareImage
from cato_common.domain.compare_image_result import CompareImageResult
from tests.utils import mock_safe


@pytest.fixture
def test_context():
    class TestContext:
        def __init__(self):
            self.counter = 0
            self.mock_store_image = mock_safe(StoreImage)
            self.mock_store_image.store_image.side_effect = self._mocked_store_image
            self.mock_image_comparator = mock_safe(SsimImageComparator)
            self.mock_file_storage = mock_safe(AbstractFileStorage)
            self.comparison_result = ComparisonResult(
                status=ResultStatus.SUCCESS, message="", diff_image="some-path", error=1
            )
            self.comparison_settings = ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=1
            )
            self.mock_image_comparator.compare.return_value = self.comparison_result
            self.mock_file_storage.find_by_id.side_effect = lambda x: File(
                id=x, name=f"{x}.png", hash="1", value_counter=0
            )
            self.mock_file_storage.get_read_stream.side_effect = lambda x: BytesIO(
                b"output image" if x == 1 else b"reference image"
            )
            self.compare_image = CompareImage(
                self.mock_store_image,
                self.mock_image_comparator,
                self.mock_file_storage,
            )

        def _mocked_store_image(self, path):
            self.counter += 1
            return Image(
                id=self.counter,
                name="test",
                original_file_id=1,
                channels=[],
                width=10,
                height=20,
                transcoding_state=ImageTranscodingState.TRANSCODED,
            )

    return TestContext()


class TestCompareImage:
    def test_compare_images_successfully(self, test_context):
        result = test_context.compare_image.compare_image(
            BytesIO(b"output image"),
            "output.png",
            BytesIO(b"reference image"),
            "reference.png",
            test_context.comparison_settings,
        )

        assert result == CompareImageResult(
            status=test_context.comparison_result.status,
            message=test_context.comparison_result.message,
            reference_image_id=2,
            output_image_id=1,
            diff_image_id=3,
            error=1,
        )
        assert test_context.mock_store_image.store_image.call_count == 3
        assert test_context.mock_image_comparator.compare.call_args[0][0].endswith(
            "reference.png"
        )
        assert test_context.mock_image_comparator.compare.call_args[0][1].endswith(
            "output.png"
        )
        assert (
            test_context.mock_image_comparator.compare.call_args[0][0]
            != test_context.mock_image_comparator.compare.call_args[0][1]
        )
        assert (
            test_context.mock_image_comparator.compare.call_args[0][2]
            == test_context.comparison_settings
        )

    def test_compare_images_from_db_successfully(self, test_context):
        test_context.mock_file_storage.find_by_id.side_effect = lambda x: File(
            id=x, name=f"{x}.png", hash="1", value_counter=0
        )
        test_context.mock_file_storage.get_read_stream.side_effect = lambda x: BytesIO(
            b"output image"
        )
        result = test_context.compare_image.compare_image_from_db(
            Image(
                id=1,
                name="output.png",
                original_file_id=10,
                channels=[],
                width=1920,
                height=1080,
                transcoding_state=ImageTranscodingState.TRANSCODED,
            ),
            Image(
                id=2,
                name="reference.png",
                original_file_id=20,
                channels=[],
                width=1920,
                height=1080,
                transcoding_state=ImageTranscodingState.TRANSCODED,
            ),
            test_context.comparison_settings,
        )

        assert result == CompareImageResult(
            status=test_context.comparison_result.status,
            message=test_context.comparison_result.message,
            reference_image_id=2,
            output_image_id=1,
            diff_image_id=1,
            error=1,
        )
        assert test_context.mock_store_image.store_image.call_count == 1
        assert test_context.mock_image_comparator.compare.call_args[0][0].endswith(
            "reference.png"
        )
        assert test_context.mock_image_comparator.compare.call_args[0][1].endswith(
            "output.png"
        )
        assert (
            test_context.mock_image_comparator.compare.call_args[0][0]
            != test_context.mock_image_comparator.compare.call_args[0][1]
        )
        assert (
            test_context.mock_image_comparator.compare.call_args[0][2]
            == test_context.comparison_settings
        )

    def test_compare_images_failure(self, test_context):
        test_context.mock_image_comparator.compare.return_value = ComparisonResult(
            status=ResultStatus.FAILED,
            message="Failed",
            diff_image="some-path",
            error=1,
        )

        result = test_context.compare_image.compare_image(
            BytesIO(b"output image"),
            "output.png",
            BytesIO(b"reference image"),
            "reference.png",
            test_context.comparison_settings,
        )

        assert result == CompareImageResult(
            status=ResultStatus.FAILED,
            message="Failed",
            reference_image_id=2,
            output_image_id=1,
            diff_image_id=3,
            error=1,
        )
        assert test_context.mock_store_image.store_image.call_count == 3
        assert test_context.mock_image_comparator.compare.call_args[0][0].endswith(
            "reference.png"
        )
        assert test_context.mock_image_comparator.compare.call_args[0][1].endswith(
            "output.png"
        )
        assert (
            test_context.mock_image_comparator.compare.call_args[0][0]
            != test_context.mock_image_comparator.compare.call_args[0][1]
        )
        assert (
            test_context.mock_image_comparator.compare.call_args[0][2]
            == test_context.comparison_settings
        )

    def test_compare_images_failure_with_no_diff_image(self, test_context):
        test_context.mock_image_comparator.compare.return_value = ComparisonResult(
            status=ResultStatus.FAILED,
            message="Failed",
            diff_image=None,
            error=0,
        )

        result = test_context.compare_image.compare_image(
            BytesIO(b"output image"),
            "output.png",
            BytesIO(b"reference image"),
            "reference.png",
            test_context.comparison_settings,
        )

        assert result == CompareImageResult(
            status=ResultStatus.FAILED,
            message="Failed",
            reference_image_id=2,
            output_image_id=1,
            diff_image_id=None,
            error=0,
        )

    def test_compare_images_from_db_failure(self, test_context):
        test_context.mock_image_comparator.compare.return_value = ComparisonResult(
            status=ResultStatus.FAILED,
            message="Failed",
            diff_image="some-path",
            error=1,
        )

        result = test_context.compare_image.compare_image_from_db(
            Image(
                id=1,
                name="output.png",
                original_file_id=10,
                channels=[],
                width=1920,
                height=1080,
                transcoding_state=ImageTranscodingState.TRANSCODED,
            ),
            Image(
                id=2,
                name="reference.png",
                original_file_id=20,
                channels=[],
                width=1920,
                height=1080,
                transcoding_state=ImageTranscodingState.TRANSCODED,
            ),
            test_context.comparison_settings,
        )

        assert result == CompareImageResult(
            status=ResultStatus.FAILED,
            message="Failed",
            reference_image_id=2,
            output_image_id=1,
            diff_image_id=1,
            error=1,
        )
        assert test_context.mock_store_image.store_image.call_count == 1
        assert test_context.mock_image_comparator.compare.call_args[0][0].endswith(
            "reference.png"
        )
        assert test_context.mock_image_comparator.compare.call_args[0][1].endswith(
            "output.png"
        )
        assert (
            test_context.mock_image_comparator.compare.call_args[0][0]
            != test_context.mock_image_comparator.compare.call_args[0][1]
        )
        assert (
            test_context.mock_image_comparator.compare.call_args[0][2]
            == test_context.comparison_settings
        )

    def test_compare_images_from_db_failure_with_no_diff_image(self, test_context):
        test_context.mock_image_comparator.compare.return_value = ComparisonResult(
            status=ResultStatus.FAILED,
            message="Failed",
            diff_image=None,
            error=0,
        )

        result = test_context.compare_image.compare_image_from_db(
            Image(
                id=1,
                name="output.png",
                original_file_id=10,
                channels=[],
                width=1920,
                height=1080,
                transcoding_state=ImageTranscodingState.TRANSCODED,
            ),
            Image(
                id=2,
                name="reference.png",
                original_file_id=20,
                channels=[],
                width=1920,
                height=1080,
                transcoding_state=ImageTranscodingState.TRANSCODED,
            ),
            test_context.comparison_settings,
        )

        assert result == CompareImageResult(
            status=ResultStatus.FAILED,
            message="Failed",
            reference_image_id=2,
            output_image_id=1,
            diff_image_id=None,
            error=0,
        )

    def test_compare_images_from_db_no_output_image(self, test_context):
        test_context.mock_file_storage.find_by_id.side_effect = lambda x: (
            File(id=x, name=f"{x}.png", hash="1", value_counter=0) if x == 10 else None
        )

        with pytest.raises(ValueError):
            test_context.compare_image.compare_image_from_db(
                Image(
                    id=1,
                    name="output.png",
                    original_file_id=10,
                    channels=[],
                    width=1920,
                    height=1080,
                    transcoding_state=ImageTranscodingState.TRANSCODED,
                ),
                Image(
                    id=2,
                    name="reference.png",
                    original_file_id=20,
                    channels=[],
                    width=1920,
                    height=1080,
                    transcoding_state=ImageTranscodingState.TRANSCODED,
                ),
                test_context.comparison_settings,
            )

    def test_compare_images_from_db_no_reference_image(self, test_context):
        test_context.mock_file_storage.find_by_id.side_effect = lambda x: (
            File(id=x, name=f"{x}.png", hash="1", value_counter=0) if x == 20 else None
        )

        with pytest.raises(ValueError):
            test_context.compare_image.compare_image_from_db(
                Image(
                    id=1,
                    name="output.png",
                    original_file_id=10,
                    channels=[],
                    width=1920,
                    height=1080,
                    transcoding_state=ImageTranscodingState.TRANSCODED,
                ),
                Image(
                    id=2,
                    name="reference.png",
                    original_file_id=20,
                    channels=[],
                    width=1920,
                    height=1080,
                    transcoding_state=ImageTranscodingState.TRANSCODED,
                ),
                test_context.comparison_settings,
            )

    def test_compare_images_with_same_name(self, test_context):
        result = test_context.compare_image.compare_image(
            BytesIO(b"output image"),
            "an_image.png",
            BytesIO(b"reference image"),
            "an_image.png",
            ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1),
        )

        assert result == CompareImageResult(
            status=test_context.comparison_result.status,
            message=test_context.comparison_result.message,
            reference_image_id=2,
            output_image_id=1,
            diff_image_id=3,
            error=1,
        )
        assert test_context.mock_store_image.store_image.call_count == 3
        assert test_context.mock_image_comparator.compare.call_args[0][0].endswith(
            "an_image.png"
        )
        assert test_context.mock_image_comparator.compare.call_args[0][1].endswith(
            "an_image.png"
        )
        assert (
            test_context.mock_image_comparator.compare.call_args[0][0]
            != test_context.mock_image_comparator.compare.call_args[0][1]
        )
        assert (
            test_context.mock_image_comparator.compare.call_args[0][2]
            == test_context.comparison_settings
        )
