import pytest

from cato_server.configuration.oidc_config import OidcConfiguration
from cato_server.domain.auth.secret_str import SecretStr
from tests.integrationtests.cato_server import testcontainers_test


@pytest.fixture
def oidc_configuration(keycloak_with_realm_and_users):
    keycloak_server_url = (
        keycloak_with_realm_and_users.keycloak_container.get_connection_url()
    )
    return OidcConfiguration(
        client_id="cato-dev-login",
        client_secret=SecretStr("this-is-a-secret"),
        well_known_url=f"{keycloak_server_url}/realms/cato-dev/.well-known/openid-configuration",
    )


@pytest.fixture
def live_server_with_keycloak(
    live_server, app_and_config_fixture, keycloak_with_realm_and_users
):
    app, config = app_and_config_fixture
    keycloak_with_realm_and_users.keycloak_admin.update_client(
        "f042a308-9cc0-4b62-b231-eadbbea9d69e",
        {"redirectUris": [f"http://127.0.0.1:{config.port}/*"]},
    )
    yield live_server


@testcontainers_test
def test_login_via_keycloak(live_server_with_keycloak, selenium_driver):
    selenium_driver.get(f"{live_server_with_keycloak.server_url()}")

    selenium_driver.find_element_by_id("login").click()
    _login_with_test_user(selenium_driver)

    selenium_driver.find_element_by_xpath("//*[text()='test_name']")

    # todo verify user information once whoami route is implemented


@testcontainers_test
def test_login_from_project_url_should_land_on_project_page(
    live_server_with_keycloak, selenium_driver, project
):
    selenium_driver.get(f"{live_server_with_keycloak.server_url()}/projects/1")

    selenium_driver.find_element_by_id("login").click()
    _login_with_test_user(selenium_driver)

    selenium_driver.wait_until(
        lambda driver: driver.current_url.endswith("/projects/1")
    )
    selenium_driver.wait_until(
        lambda driver: driver.find_element_by_tag_name("h1").text == "test_name"
    )


@testcontainers_test
def test_login_from_login_url_should_land_on_home(
    live_server_with_keycloak, selenium_driver, project
):
    selenium_driver.get(f"{live_server_with_keycloak.server_url()}/login")

    _login_with_test_user(selenium_driver)

    selenium_driver.find_element_by_xpath("//*[text()='test_name']")
    assert selenium_driver.current_url == f"{live_server_with_keycloak.server_url()}/"


def _login_with_test_user(selenium_driver):
    selenium_driver.find_element_by_id("username").send_keys("test")
    selenium_driver.find_element_by_id("password").send_keys("password")
    selenium_driver.find_element_by_id("kc-login").click()
