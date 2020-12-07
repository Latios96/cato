import logging

from flask import Blueprint, jsonify

import cato_server
from cato_server.configuration.app_configuration import AppConfiguration

logger = logging.getLogger(__name__)


class AboutBlueprint(Blueprint):
    def __init__(self, app_configuration: AppConfiguration):
        super(AboutBlueprint, self).__init__("about", __name__)
        self._app_configuration = app_configuration

        self.route("/about", methods=["GET"])(self.about)

    def about(self):
        version = cato_server.__version__
        if self._app_configuration.debug:
            version+="-dev"
        return jsonify({
            'version': version
        })
