import logging

import requests
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from cato_server.configuration.app_configuration import AppConfiguration

logger = logging.getLogger(__name__)


class BackgroundTaskCreator:
    def create(self, app: FastAPI, app_configuration: AppConfiguration):
        logger.info("Creating background tasks..")

        base_url = f"http://127.0.0.1:{app_configuration.port}"

        def query_task_url(task_url: str):
            response = requests.get(f"{base_url}/api/v1" + task_url)
            if response.status_code != 200:
                logger.error(
                    f'Error when executing task "fail_timed_out_tests_tasks": {response}'
                )

        @app.on_event("startup")
        @repeat_every(seconds=120)
        def fail_timed_out_tests_tasks() -> None:
            query_task_url("/background_tasks/fail_timed_out_tests")

        logger.info("Created task fail_timed_out_tests..")

        logger.info("Created background tasks.")
