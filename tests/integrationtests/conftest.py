import os
import socket
import threading
import time
from typing import Callable

import pytest
import uvicorn
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType


class LiveServer:
    def __init__(self, app, port, startup_timeout):
        self._app = app
        self._port = port
        self._startup_timeout = startup_timeout
        self.server = None

    def spawn_live_server(self):
        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                print(f"Running server on port {self._port}")
                config = uvicorn.Config(self._app, host="127.0.0.1", port=self._port)
                self.server = uvicorn.Server(config)
                self.server.run()

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
        self.server.should_exit = True

    def server_url(self):
        return f"http://127.0.0.1:{self._port}"


@pytest.fixture
def live_server(app_and_config_fixture, project):
    app, config = app_and_config_fixture
    live_server = LiveServer(app, config.port, 10)
    live_server.spawn_live_server()
    yield live_server
    live_server.terminate()


class MyChromeDriver(webdriver.Chrome):
    def find_element_by_css_module_class_name(self, class_name: str):
        return self.find_element_by_css_selector(f'[class^="{class_name}"]')

    def wait_until(self, predicate: Callable[[webdriver.Chrome], bool]):
        return WebDriverWait(self, 10).until(predicate)


@pytest.fixture
def selenium_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver_path = (
        ChromeDriverManager(
            chrome_type=ChromeType.GOOGLE,
        ).install()
        if not os.environ.get("CI")
        else os.path.join(os.environ["CHROMEWEBDRIVER"], "chromedriver")
    )
    driver = MyChromeDriver(
        executable_path=driver_path,
        options=chrome_options,
    )
    driver.implicitly_wait(5)
    yield driver
    driver.close()
