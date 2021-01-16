class HomePage:
    def __init__(self, stateless_test):
        self.stateless_test = stateless_test

    def the_link_card_for_the_project_should_be_displayed(self):
        link_card = (
            self.stateless_test.selenium_driver.find_element_by_css_module_class_name(
                "LinkCard_cardContentDiv"
            )
        )
        assert link_card.text == self.stateless_test.project.name

    def when_clicking_the_card_it_should_navigate_to_project_page(self):
        link_card = (
            self.stateless_test.selenium_driver.find_element_by_css_module_class_name(
                "LinkCard_cardContentDiv"
            )
        )
        link_card.click()


class ProjectPage:
    def __init__(self, stateless_test):
        self.stateless_test = stateless_test

    def the_project_name_should_be_visible(self):
        project_name = self.stateless_test.selenium_driver.find_element_by_tag_name(
            "h1"
        )
        assert project_name.text == self.stateless_test.project.name

    def select_a_run_placeholder_should_be_visible(self):
        placeholder = (
            self.stateless_test.selenium_driver.find_element_by_css_module_class_name(
                "ProjectRunsView_suiteResultsPlaceholder"
            )
        )
        assert placeholder.text == "Please select a run"


class ReadOnlySeleniumTest:
    def __init__(self, live_server, selenium_driver, project, test_result):
        self.live_server = live_server
        self.selenium_driver = selenium_driver
        self.project = project
        self.test_result = test_result
        self.home_page = HomePage(self)
        self.project_page = ProjectPage(self)

    def execute(self):
        raise NotImplementedError()

    def navigate_to_home(self):
        self.selenium_driver.get(self.live_server.server_url())
        self.selenium_driver.find_element_by_css_module_class_name(
            "LinkCard_cardContentDiv"
        )

    def when_clicking_on_cato_in_header_it_should_navigate_to_home(self):
        header_link = self.selenium_driver.find_element_by_css_module_class_name(
            "Header_logoCato"
        )
        header_link.click()
        assert self.selenium_driver.current_url == self.live_server.server_url() + "/#/"

    def navigate_to_project_page(self):
        self.navigate_to_home()
        self.home_page.the_link_card_for_the_project_should_be_displayed()
        self.home_page.when_clicking_the_card_it_should_navigate_to_project_page()
        self.project_page.the_project_name_should_be_visible()


class ProjectPageShouldNavigateToProjectTest(ReadOnlySeleniumTest):
    def execute(self):
        self.navigate_to_home()
        self.home_page.the_link_card_for_the_project_should_be_displayed()
        self.home_page.when_clicking_the_card_it_should_navigate_to_project_page()
        self.project_page.the_project_name_should_be_visible()
        self.when_clicking_on_cato_in_header_it_should_navigate_to_home()
        self.home_page.the_link_card_for_the_project_should_be_displayed()


class NavigateBackAndForwardShouldWorkTest(ReadOnlySeleniumTest):
    def execute(self):
        self.navigate_to_home()
        self.home_page.the_link_card_for_the_project_should_be_displayed()
        self.home_page.when_clicking_the_card_it_should_navigate_to_project_page()
        self.project_page.the_project_name_should_be_visible()
        self.selenium_driver.back()
        self.home_page.the_link_card_for_the_project_should_be_displayed()
        self.selenium_driver.forward()
        self.project_page.the_project_name_should_be_visible()


class DisplayProjectPage(ReadOnlySeleniumTest):
    def execute(self):
        self.navigate_to_project_page()
        self.project_page.select_a_run_placeholder_should_be_visible()


def test_read_only_tests(live_server, selenium_driver, project, test_result):
    test = ProjectPageShouldNavigateToProjectTest(
        live_server, selenium_driver, project, test_result
    )
    test.execute()

    test = NavigateBackAndForwardShouldWorkTest(
        live_server, selenium_driver, project, test_result
    )
    test.execute()


def test_display(live_server, selenium_driver, project, test_result):
    test = DisplayProjectPage(live_server, selenium_driver, project, test_result)
    test.execute()
