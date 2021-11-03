from typing import cast, TypeVar, Type, List

from cato.domain.config import RunConfig
from cato.runners.sync_comparison_settings import SyncComparisonSettings
from cato.runners.sync_reference_image_edits import SyncReferenceImageEdits
from cato_api_client.cato_api_client import CatoApiClient
from cato_common.domain.test_edit import (
    EditTypes,
    ComparisonSettingsEdit,
    ReferenceImageEdit,
)

T = TypeVar("T")


class SyncTestEdits:
    def __init__(
        self,
        cato_api_client: CatoApiClient,
        sync_comparison_settings: SyncComparisonSettings,
        sync_reference_image_edits: SyncReferenceImageEdits,
    ):
        self._cato_api_client = cato_api_client
        self._update_comparison_settings = sync_comparison_settings
        self._sync_reference_images = sync_reference_image_edits

    def update(self, config: RunConfig, path: str, run_id):
        all_test_edits = self._cato_api_client.get_test_edits_to_sync_for_run(run_id)

        all_comparison_settings_edits = self._filter_edits_by(
            all_test_edits, EditTypes.COMPARISON_SETTINGS, ComparisonSettingsEdit
        )
        self._update_comparison_settings.update(
            config, path, all_comparison_settings_edits
        )

        all_reference_image_edits = self._filter_edits_by(
            all_test_edits, EditTypes.REFERENCE_IMAGE, ReferenceImageEdit
        )
        self._sync_reference_images.update(config, all_reference_image_edits)

    def _filter_edits_by(
        self, all_test_edits, edit_type: EditTypes, edit_class: Type[T]
    ) -> List[T]:
        return list(
            map(
                lambda x: cast(edit_class, x),
                filter(
                    lambda x: x.edit_type == edit_type,
                    all_test_edits,
                ),
            )
        )
