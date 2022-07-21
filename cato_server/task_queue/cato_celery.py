import time

from celery import Celery

from cato_server.configuration.app_configuration import AppConfiguration


class CatoCelery:
    def __init__(self, app_configuration: AppConfiguration):
        result_backend = (
            "db+postgresql://"
            + app_configuration.storage_configuration.database_url.split("://")[1]
        )
        self.app = Celery(
            "tasks",
            broker=app_configuration.celery_configuration.broker_url,
            result_backend=result_backend,
        )

        @self.app.task
        def hello_world():
            time.sleep(2)
            return {"hello": "world"}

        self.hello_world = hello_world
