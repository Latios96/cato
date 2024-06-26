from selenium.webdriver.common.by import By


def test_logout_successfully(authenticated_selenium_driver, live_server):
    authenticated_selenium_driver.get(live_server.server_url())

    authenticated_selenium_driver.find_element(By.ID, "btn-about-user-menu").click()
    authenticated_selenium_driver.find_element(By.ID, "about-user-menu-logout").click()

    authenticated_selenium_driver.find_element(By.ID, "login")
    assert authenticated_selenium_driver.current_url == f"{live_server.server_url()}/"


def test_logout_successfully_from_subpage_should_return_to_root_url(
    authenticated_selenium_driver, live_server
):
    authenticated_selenium_driver.get(f"{live_server.server_url()}/projects/1")

    authenticated_selenium_driver.find_element(By.ID, "btn-about-user-menu").click()
    authenticated_selenium_driver.find_element(By.ID, "about-user-menu-logout").click()

    authenticated_selenium_driver.find_element(By.ID, "login")
    assert authenticated_selenium_driver.current_url == f"{live_server.server_url()}/"
