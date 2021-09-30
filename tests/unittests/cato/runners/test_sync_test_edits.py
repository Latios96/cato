from cato.runners.sync_comparison_settings import SyncComparisonSettings
from cato.runners.sync_reference_image_edits import SyncReferenceImageEdits
from cato.runners.sync_test_edits import SyncTestEdits
from cato_api_client.cato_api_client import CatoApiClient
from cato_common.domain.test_identifier import TestIdentifier
from tests.unittests.cato.runners.test_sync_comparison_settings import (
    create_comparison_settings_edit,
)
from tests.unittests.cato.runners.test_sync_reference_image_edits import (
    create_reference_image_edit,
)
from tests.utils import mock_safe


def test_sync_edits(config_fixture):
    reference_image_edit = create_reference_image_edit(
        TestIdentifier.from_string("some/test")
    )
    comparison_settings_edit = create_comparison_settings_edit(
        TestIdentifier.from_string("some/other_test")
    )
    mock_cato_api_client = mock_safe(CatoApiClient)
    mock_cato_api_client.get_test_edits_to_sync_for_run.return_value = [
        reference_image_edit,
        comparison_settings_edit,
    ]
    mock_update_comparison_settings = mock_safe(SyncComparisonSettings)
    mock_sync_reference_images = mock_safe(SyncReferenceImageEdits)
    sync_test_edits = SyncTestEdits(
        mock_cato_api_client,
        mock_update_comparison_settings,
        mock_sync_reference_images,
    )

    sync_test_edits.update(config_fixture.RUN_CONFIG, "the_path.json", 1)

    mock_update_comparison_settings.update.assert_called_with(
        config_fixture.RUN_CONFIG, "the_path.json", [comparison_settings_edit]
    )
    mock_sync_reference_images.update.assert_called_with(
        config_fixture.RUN_CONFIG, [reference_image_edit]
    )
