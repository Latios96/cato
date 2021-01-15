import socket
import threading
import time

import pytest
import requests
from flask import request


class LiveServer:
    def __init__(self, app, port, startup_timeout):
        self._app = app
        self._port = port
        self._startup_timeout = startup_timeout

    def spawn_live_server(self):
        def shutdown_server():
            func = request.environ.get("werkzeug.server.shutdown")
            if func is None:
                raise RuntimeError("Not running with the Werkzeug Server")
            func()

        @self._app.route("/shutdown", methods=["GET"])
        def shutdown():
            shutdown_server()
            return "Server shutting down..."

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                self._app.run(port=self._port, use_reloader=False)

        continuous_thread = ScheduleThread()
        continuous_thread.start()

        start_time = time.time()

        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > self._startup_timeout:
                raise RuntimeError(
                    "Failed to start the server after %d seconds. "
                    % self._startup_timeout
                )

            if self._can_ping_server():
                break

    def _can_ping_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(("localhost", self._port))
        except socket.error as e:
            success = False
        else:
            success = True
        finally:
            sock.close()

        return success

    def terminate(self):
        requests.get(self.server_url() + "/shutdown")

    def server_url(self):
        return f"http://localhost:{self._port}"


@pytest.fixture
def live_server(app_and_config_fixture, project):
    app, config = app_and_config_fixture
    live_server = LiveServer(app, config.port, 10)
    live_server.spawn_live_server()
    yield live_server
    live_server.terminate()


def test_start(live_server):
    response = requests.get(live_server.server_url() + "/api/v1/projects")
    assert response.json() == [{"id": 1, "name": "test_name"}]
    assert response.status_code == 200
