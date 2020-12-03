import logging
import os
import tempfile

from flask import Blueprint, jsonify, request, send_file

from cato.storage.abstract.abstract_file_storage import AbstractFileStorage
from oiio.OpenImageIO import ImageBuf

logger = logging.getLogger(__name__)


class TestResultsBlueprint(Blueprint):
    def __init__(self, file_storage: AbstractFileStorage):
        super(TestResultsBlueprint, self).__init__("test-results", __name__)
        self._file_storage = file_storage

