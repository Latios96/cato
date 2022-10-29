import datetime
import os
import socket
import threading
import time
from dataclasses import dataclass
from typing import Callable, List

import pytest
import requests
import uvicorn
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

from cato_common.utils.datetime_utils import aware_now_in_utc


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


@dataclass
class Cookie:
    name: str
    value: str
    domain: str = "127.0.0.1"
    expires: datetime.datetime = aware_now_in_utc() + datetime.timedelta(hours=2)
    http_only: bool = True
    path: str = "/"
    same_site: str = "Lax"
    secure: bool = False


class MyChromeDriver(webdriver.Chrome):
    def set_startup_cookies(self, cookies: List[Cookie]):
        self.execute_cdp_cmd("Network.enable", {})

        for cookie in cookies:
            cookie_dict = {
                "name": cookie.name,
                "value": cookie.value,
                "domain": cookie.domain,
                "expires": int(cookie.expires.timestamp()),
                "httpOnly": cookie.http_only,
                "path": cookie.path,
                "sameSite": cookie.same_site,
                "secure": cookie.secure,
            }
            self.execute_cdp_cmd("Network.setCookie", cookie_dict)

        self.execute_cdp_cmd("Network.disable", {})

    def find_element_by_css_module_class_name(self, class_name: str):
        return self.find_element(By.CSS_SELECTOR, f'[class^="{class_name}"]')

    def wait_until(self, predicate: Callable[[webdriver.Chrome], bool], timeout=20):
        return WebDriverWait(self, timeout).until(
            wrap_catch_webdriver_exceptions(predicate)
        )

    def wait_until_not(self, predicate: Callable[[webdriver.Chrome], bool], timeout=20):
        return WebDriverWait(self, timeout).until_not(
            wrap_catch_webdriver_exceptions(predicate)
        )


def wrap_catch_webdriver_exceptions(predicate: Callable[[webdriver.Chrome], bool]):
    def func(driver):
        try:
            return predicate(driver)
        except WebDriverException:
            return False

    return func


@pytest.fixture
def selenium_driver() -> MyChromeDriver:
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


@pytest.fixture
def authenticated_selenium_driver(selenium_driver, http_session_cookie):
    session_cookie_name, cookie_value = http_session_cookie
    selenium_driver.set_startup_cookies(
        [Cookie(name=session_cookie_name, value=cookie_value)]
    )
    yield selenium_driver


@pytest.fixture
def authenticated_requests_session(http_session_cookie, crsf_token):
    session_cookie_name, session_cookie_value = http_session_cookie

    session = requests.Session()
    session.cookies.set(session_cookie_name, session_cookie_value)
    session.cookies["XSRF-TOKEN"] = crsf_token
    session.headers["X-XSRF-TOKEN"] = crsf_token

    return session
