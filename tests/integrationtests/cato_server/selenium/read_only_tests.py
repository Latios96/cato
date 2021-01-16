import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select

from tests.integrationtests.cato_server.conftest import MyChromeDriver


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

    def should_display_run_list(self):
        run_number = (
            self.stateless_test.selenium_driver.find_element_by_css_module_class_name(
                "ProjectRunsView_runNumber"
            )
        )
        assert run_number.text == "Run #1"

    def select_run(self):
        run_number = (
            self.stateless_test.selenium_driver.find_element_by_css_module_class_name(
                "ProjectRunsView_runNumber"
            )
        )
        run_number.click()
        self.stateless_test.assert_current_url_is("/#/projects/1/runs/1/suites")


class RunView:
    def __init__(self, stateless_test):
        self.stateless_test = stateless_test

    def should_show_run_headline(self):
        run_summary_headline = (
            self.stateless_test.selenium_driver.find_element_by_css_module_class_name(
                "RunSummary_runSummaryHeadline"
            )
        )
        assert run_summary_headline.text == "Run Summary: #1"

    def the_suites_tab_should_be_selected(self):
        suites_tab = self.stateless_test.selenium_driver.find_element_by_id(
            "controlled-tab-example-tab-suites"
        )
        assert suites_tab.get_attribute("class") == "nav-item nav-link active"

    def the_suites_tab_should_display_one_entry(self):
        suite_list = self.stateless_test.selenium_driver.find_elements_by_css_selector(
            f'[class^="SuiteAndTestLists_listEntry"]'
        )
        assert len(suite_list) == 1
        assert suite_list[0].find_elements_by_tag_name("span")[1].text == "my_suite"

    def clicking_on_suite_entry_should_show_suite_tests(self):
        suite_list = self.stateless_test.selenium_driver.find_elements_by_css_selector(
            f'[class^="SuiteAndTestLists_listEntry"]'
        )
        suite_list[0].click()
        self.stateless_test.assert_current_url_is("/#/projects/1/runs/1/suites/1")

    def the_breadcrumb_should_be_shown(self):
        time.sleep(0.5)
        breadcrumb_entries = (
            self.stateless_test.selenium_driver.find_elements_by_class_name(
                "breadcrumb-item"
            )
        )
        assert len(breadcrumb_entries) == 2
        assert breadcrumb_entries[0].find_element_by_tag_name("a").text == "Run #1"
        assert breadcrumb_entries[1].find_element_by_tag_name("a").text == "my_suite"

    def the_suites_tests_should_be_shown(self):
        suite_list = self.stateless_test.selenium_driver.find_elements_by_css_selector(
            f'[class^="SuiteAndTestLists_listEntry"]'
        )
        assert len(suite_list) == 1
        assert (
            suite_list[0].find_elements_by_tag_name("span")[1].text
            == "my_suite/my_test_name"
        )

    def clicking_on_test_name_in_test_list_should_show_test(self):
        suite_list = self.stateless_test.selenium_driver.find_elements_by_css_selector(
            f'[class^="SuiteAndTestLists_listEntry"]'
        )

        suite_list[0].click()
        self.stateless_test.assert_current_url_is("/#/projects/1/runs/1/tests/1")

    def the_breadcrumb_should_be_shown_and_show_test_name(self):
        time.sleep(0.5)
        breadcrumb_entries = (
            self.stateless_test.selenium_driver.find_elements_by_class_name(
                "breadcrumb-item"
            )
        )
        assert len(breadcrumb_entries) == 3
        assert breadcrumb_entries[0].find_element_by_tag_name("a").text == "Run #1"
        assert breadcrumb_entries[1].find_element_by_tag_name("a").text == "my_suite"
        assert (
            breadcrumb_entries[2].find_element_by_tag_name("a").text == "my_test_name"
        )

    def should_navigate_to_suite_by_breadcrumb(self):
        time.sleep(0.5)
        breadcrumb_entries = (
            self.stateless_test.selenium_driver.find_elements_by_class_name(
                "breadcrumb-item"
            )
        )
        breadcrumb_entries[1].click()
        self.stateless_test.assert_current_url_is("/#/projects/1/runs/1/suites/1")

    def should_navigate_to_run_by_breadcrumb(self):
        time.sleep(0.5)
        breadcrumb_entries = (
            self.stateless_test.selenium_driver.find_elements_by_class_name(
                "breadcrumb-item"
            )
        )
        breadcrumb_entries[0].click()
        self.stateless_test.assert_current_url_is("/#/projects/1/runs/1")

    def select_tests_tab(self):
        self.stateless_test.selenium_driver.find_element_by_id(
            "controlled-tab-example-tab-tests"
        ).click()
        self.stateless_test.assert_current_url_is("/#/projects/1/runs/1/tests")

    def the_tests_tab_should_display_one_entry(self):
        time.sleep(0.5)
        tests_list = self.stateless_test.selenium_driver.find_elements_by_css_selector(
            f'[class^="SuiteAndTestLists_listEntry"]'
        )
        assert (
            tests_list[1].find_elements_by_tag_name("span")[1].text
            == "my_suite/my_test_name"
        )

    def clicking_on_test_name_in_test_tab_should_show_test(self):
        suite_list = self.stateless_test.selenium_driver.find_elements_by_css_selector(
            f'[class^="SuiteAndTestLists_listEntry"]'
        )
        suite_list[1].click()
        self.stateless_test.assert_current_url_is("/#/projects/1/runs/1/tests/1")


class TestResultPage:
    def __init__(self, stateless_test):
        self.stateless_test = stateless_test

    def should_display_test_duration(self, duration):
        assert (
            self.stateless_test.selenium_driver.find_element_by_id(
                "test-duration-value"
            ).text
            == duration
        )

    def show_log_button_should_be_visible(self):
        assert self.get_log_button()

    def get_log_button(self):
        return (
            self.stateless_test.selenium_driver.find_element_by_css_module_class_name(
                "DisplayLogComponent_logButton"
            )
        )

    def clicking_show_log_should_show_log(self):
        self.get_log_button().click()
        assert (
            self.stateless_test.selenium_driver.find_element_by_css_module_class_name(
                "LogComponent_terminalContent"
            )
        )

    def clicking_show_log_should_hide_log(self):
        self.get_log_button().click()
        time.sleep(0.5)
        try:
            self.stateless_test.selenium_driver.find_element_by_css_module_class_name(
                "LogComponent_terminalContent"
            )
        except NoSuchElementException:
            pass

    def channel_dropdown_should_contain_channels(self, channels):
        dropdown = (
            self.stateless_test.selenium_driver.find_element_by_css_module_class_name(
                "MultiChannelImageComparion_selectChannel"
            )
        )
        options = dropdown.find_elements_by_tag_name("option")
        for i, channel in enumerate(channels):
            assert options[i].text == channel

    def change_channel_to_alpha(self):
        dropdown = Select(
            self.stateless_test.selenium_driver.find_element_by_css_module_class_name(
                "MultiChannelImageComparion_selectChannel"
            )
        )
        dropdown.select_by_visible_text("alpha")

    def alpha_image_should_be_shown(self):
        images = self.stateless_test.selenium_driver.find_element_by_id(
            "ImageCompariontest"
        ).find_elements_by_tag_name("img")
        assert (
            images[0].get_attribute("src")
            == self.stateless_test.live_server.server_url() + "/api/v1/files/2"
        )

    def rgb_channel_should_be_selected_and_shown(self):
        dropdown = Select(
            self.stateless_test.selenium_driver.find_element_by_css_module_class_name(
                "MultiChannelImageComparion_selectChannel"
            )
        )
        assert dropdown.first_selected_option.text == "rgb"
        images = self.stateless_test.selenium_driver.find_element_by_id(
            "ImageCompariontest"
        ).find_elements_by_tag_name("img")
        assert (
            images[0].get_attribute("src")
            == self.stateless_test.live_server.server_url() + "/api/v1/files/1"
        )


class ReadOnlySeleniumTest:
    def __init__(
        self, live_server, selenium_driver: MyChromeDriver, project, test_result
    ):
        self.live_server = live_server
        self.selenium_driver = selenium_driver
        self.project = project
        self.test_result = test_result
        self.home_page = HomePage(self)
        self.project_page = ProjectPage(self)
        self.run_view = RunView(self)
        self.test_result_page = TestResultPage(self)

    def execute(self):
        raise NotImplementedError()

    def assert_current_url_is(self, url):
        assert self.selenium_driver.current_url == self.live_server.server_url() + url

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
        self.assert_current_url_is("/#/")

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


class ProjectPageNavigation(ReadOnlySeleniumTest):
    def execute(self):
        self.navigate_to_project_page_and_select_run()

        self.navigate_to_test_and_back_by_suites()

        self.navigate_to_test_and_back_by_tests()

    def navigate_to_project_page_and_select_run(self):
        self.navigate_to_project_page()
        self.project_page.select_a_run_placeholder_should_be_visible()
        self.project_page.should_display_run_list()
        self.project_page.select_run()

    def navigate_to_test_and_back_by_suites(self):
        self.run_view.should_show_run_headline()
        self.run_view.the_suites_tab_should_be_selected()
        self.run_view.the_suites_tab_should_display_one_entry()
        self.run_view.clicking_on_suite_entry_should_show_suite_tests()
        self.run_view.the_breadcrumb_should_be_shown()
        self.run_view.the_suites_tests_should_be_shown()
        self.run_view.clicking_on_test_name_in_test_list_should_show_test()
        self.run_view.the_breadcrumb_should_be_shown_and_show_test_name()
        self.run_view.should_navigate_to_suite_by_breadcrumb()
        self.run_view.should_navigate_to_run_by_breadcrumb()
        self.run_view.the_suites_tab_should_be_selected()

    def navigate_to_test_and_back_by_tests(self):
        self.run_view.select_tests_tab()
        self.run_view.the_tests_tab_should_display_one_entry()
        self.run_view.clicking_on_test_name_in_test_tab_should_show_test()


class TestResultFunctionality(ReadOnlySeleniumTest):
    def execute(self):
        self.navigate_to_test()

        self.test_result_page.should_display_test_duration("5 seconds")

        self.test_result_page.show_log_button_should_be_visible()
        self.test_result_page.clicking_show_log_should_show_log()
        self.test_result_page.clicking_show_log_should_hide_log()

        self.test_result_page.rgb_channel_should_be_selected_and_shown()
        self.test_result_page.channel_dropdown_should_contain_channels(["rgb", "alpha"])
        self.test_result_page.change_channel_to_alpha()
        self.test_result_page.alpha_image_should_be_shown()

    def navigate_to_test(self):
        self.selenium_driver.get(
            self.live_server.server_url() + "/#/projects/1/runs/1/tests/1"
        )


def test_read_only_tests(live_server, selenium_driver, project, finished_test_result):
    test = ProjectPageShouldNavigateToProjectTest(
        live_server, selenium_driver, project, finished_test_result
    )
    test.execute()

    test = NavigateBackAndForwardShouldWorkTest(
        live_server, selenium_driver, project, finished_test_result
    )
    test.execute()

    test = DisplayProjectPage(
        live_server, selenium_driver, project, finished_test_result
    )
    test.execute()

    test = ProjectPageNavigation(
        live_server, selenium_driver, project, finished_test_result
    )
    test.execute()


def test_test_result_page(
    live_server,
    selenium_driver,
    project,
    finished_test_result,
    output_for_finished_test,
):
    test = TestResultFunctionality(
        live_server, selenium_driver, project, finished_test_result
    )
    test.execute()
