import os
from typing import List

from cato.domain.config import RunConfig
from cato.domain.test import Test
from cato.domain.test_suite import filter_by_test_identifier, TestSuite
from cato.reporter.reporter import Reporter
from cato.variable_processing.variable_processor import VariableProcessor
from cato_api_client.cato_api_client import CatoApiClient
from cato_common.domain.image import Image
from cato_common.domain.test_edit import ReferenceImageEdit


class SyncReferenceImageEdits:
    def __init__(
        self,
        cato_api_client: CatoApiClient,
        variable_processor: VariableProcessor,
        reporter: Reporter,
    ):
        self._cato_api_client = cato_api_client
        self._variable_processor = variable_processor
        self._reporter = reporter

    def update(
        self,
        config: RunConfig,
        comparison_settings_edits: List[ReferenceImageEdit],
    ) -> None:
        for edit in comparison_settings_edits:
            self._update_test(config, edit)

    def _update_test(self, config, edit):
        suite, test = self._get_suite_and_test(config, edit.test_identifier)
        if not suite and not test:
            self._reporter.report_message(
                f"No test with identifier {edit.test_identifier} found in config, skipping edit.."
            )
            return
        image = self._cato_api_client.get_image_by_id(edit.new_value.reference_image_id)
        image_path = self._get_image_path(config, suite, test, image)
        image_contents = self._cato_api_client.download_original_image(
            edit.new_value.reference_image_id
        )
        if not image_contents:
            self._reporter.report_message(
                f"No new reference image found for {edit.test_identifier}, skipping edit.."
            )
            return
        self._reporter.report_message(
            f"Updating {edit.test_identifier} to a new reference image at {image_path}"
        )
        with open(image_path, "wb") as f:
            f.write(image_contents)

    def _get_suite_and_test(self, config, test_identifier):
        the_suite = filter_by_test_identifier(config.suites, test_identifier)
        if not the_suite:
            return None, None
        return the_suite[0], the_suite[0].tests[0]

    def _get_image_path(
        self, config: RunConfig, suite: TestSuite, test: Test, image: Image
    ) -> str:
        variables = self._variable_processor.evaluate_variables(config, suite, test)
        image_file_extension = os.path.splitext(image.name)[1]
        if image_file_extension == ".png":
            return variables["reference_image_png"]
        elif image_file_extension == ".exr":
            return variables["reference_image_exr"]
        else:
            return variables["reference_image_no_extension"] + image_file_extension
