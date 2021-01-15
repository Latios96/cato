def test_project_page_should_navigate_to_project(live_server, selenium_driver, project):
    navigate_to_home(live_server, selenium_driver)
    the_link_card_for_the_project_should_be_displayed(project, selenium_driver)
    when_clicking_card_it_should_navigate_to_project_page(selenium_driver)
    the_project_name_should_be_visible(project, selenium_driver)
    when_clicking_on_cato_in_header_it_should_navigate_to_home(
        live_server, selenium_driver
    )
    the_link_card_for_the_project_should_be_displayed(project, selenium_driver)


def test_nagivate_back_and_forward(live_server, selenium_driver, project):
    navigate_to_home(live_server, selenium_driver)
    the_link_card_for_the_project_should_be_displayed(project, selenium_driver)
    when_clicking_card_it_should_navigate_to_project_page(selenium_driver)
    the_project_name_should_be_visible(project, selenium_driver)
    selenium_driver.back()
    the_link_card_for_the_project_should_be_displayed(project, selenium_driver)
    selenium_driver.forward()
    the_project_name_should_be_visible(project, selenium_driver)


def when_clicking_on_cato_in_header_it_should_navigate_to_home(
    live_server, selenium_driver
):
    header_link = selenium_driver.find_element_by_css_module_class_name(
        "Header_logoCato"
    )
    header_link.click()
    assert selenium_driver.current_url == live_server.server_url() + "/#/"


def the_project_name_should_be_visible(project, selenium_driver):
    project_name = selenium_driver.find_element_by_tag_name("h1")
    assert project_name.text == project.name


def when_clicking_card_it_should_navigate_to_project_page(selenium_driver):
    link_card = selenium_driver.find_element_by_css_module_class_name(
        "LinkCard_cardContentDiv"
    )
    link_card.click()


def the_link_card_for_the_project_should_be_displayed(project, selenium_driver):
    link_card = selenium_driver.find_element_by_css_module_class_name(
        "LinkCard_cardContentDiv"
    )
    assert link_card.text == project.name


def navigate_to_home(live_server, selenium_driver):
    selenium_driver.get(live_server.server_url())
