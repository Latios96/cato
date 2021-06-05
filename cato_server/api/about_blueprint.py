import logging

from fastapi import APIRouter

import cato_server
from cato_server.configuration.app_configuration import AppConfiguration

logger = logging.getLogger(__name__)


class AboutBlueprint(APIRouter):
    def __init__(self, app_configuration: AppConfiguration):
        super(AboutBlueprint, self).__init__()
        self._app_configuration = app_configuration

        self.get("/about")(self.about)

    def about(self):
        version = cato_server.__version__
        if self._app_configuration.debug:
            version += "-dev"
        return {"version": version}
