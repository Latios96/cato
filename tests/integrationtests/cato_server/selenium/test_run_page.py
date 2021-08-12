from cato.domain.test_status import TestStatus
from cato_common.domain.execution_status import ExecutionStatus
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)
from tests.integrationtests.conftest import MyChromeDriver


class TestRunOverviewPage:
    def test_navigate_back_to_project_page(
        self, live_server, selenium_driver: MyChromeDriver, run
    ):
        self._visit_run_overview_page(live_server, run, selenium_driver)
        project_page_link = selenium_driver.find_element_by_link_text("Back to Project")

        project_page_link.click()

        assert selenium_driver.find_element_by_link_text("Run #1")

    def test_overview_page_should_auto_update(
        self,
        live_server,
        selenium_driver: MyChromeDriver,
        run,
        test_result,
        sessionmaker_fixture,
    ):
        self._visit_run_overview_page(live_server, run, selenium_driver)
        self._verify_failed_tests_count_to_be(selenium_driver, 0)
        self._fail_test(sessionmaker_fixture, test_result)
        self._verify_failed_tests_count_to_be(selenium_driver, 0)

    def _verify_failed_tests_count_to_be(self, selenium_driver, count):
        selenium_driver.find_element_by_xpath(
            f'//*[@id="runSummary failed tests-value" and text()="{count}"]'
        )

    def _fail_test(self, sessionmaker_fixture, test_result):
        repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
        test_result.status = TestStatus.FAILED
        repository.save(test_result)

    def _visit_run_overview_page(self, live_server, run, selenium_driver):
        selenium_driver.get(
            f"{live_server.server_url()}/#/projects/{run.project_id}/runs/{run.id}"
        )


class TestRunTestPage:
    def test_navigation_to_test_page_should_work(
        self, live_server, selenium_driver: MyChromeDriver, run, test_result
    ):
        self._visit_run_overview_page(live_server, run, selenium_driver)

        self._switch_to_tests_page(selenium_driver)

        self._should_display_test_result(selenium_driver, test_result)

    def test_auto_update_test_page_should_work(
        self,
        live_server,
        selenium_driver: MyChromeDriver,
        run,
        test_result,
        sessionmaker_fixture,
    ):
        self._visit_run_test_page(live_server, run, selenium_driver)

        self._assert_first_test_has_icon_with_title(selenium_driver, "not started")

        self._update_test_result_execution_status(sessionmaker_fixture, test_result)

        self._assert_first_test_has_icon_with_title(selenium_driver, "running")

    def test_selecting_a_test_should_display_the_test(
        self, live_server, selenium_driver, run, test_result
    ):
        self._visit_run_test_page(live_server, run, selenium_driver)
        self._assert_no_test_is_selected(selenium_driver)
        self._select_a_test(selenium_driver)
        self._assert_test_is_selected(selenium_driver)

    def test_selecting_a_test_should_display_should_survive_refresh(
        self, live_server, selenium_driver, run, test_result
    ):
        self._visit_run_test_page(live_server, run, selenium_driver)
        self._assert_no_test_is_selected(selenium_driver)
        self._select_a_test(selenium_driver)
        self._assert_test_is_selected(selenium_driver)
        selenium_driver.refresh()
        self._assert_test_is_selected(selenium_driver)

    def test_changing_the_test_selection_should_work(
        self,
        live_server,
        selenium_driver,
        run,
        test_result,
        test_result_factory,
        sessionmaker_fixture,
    ):
        SqlAlchemyTestResultRepository(sessionmaker_fixture).save(
            test_result_factory(
                suite_result_id=test_result.suite_result_id,
                execution_status=ExecutionStatus.RUNNING,
            )
        )
        self._visit_run_test_page(live_server, run, selenium_driver)
        self._select_a_test(selenium_driver)
        self._assert_test_is_selected(selenium_driver)
        self._select_other_test(selenium_driver)
        self._assert_other_test_is_selected(selenium_driver)

    def _assert_other_test_is_selected(self, selenium_driver):
        assert selenium_driver.find_element_by_id(
            "selectedTestContainer"
        ).find_element_by_xpath("//*[text()='started: just now']")

    def _select_other_test(self, selenium_driver):
        selenium_driver.find_element_by_xpath('//*[@id="testList"]/tbody/tr[2]').click()

    def _assert_test_is_selected(self, selenium_driver):
        assert selenium_driver.find_element_by_id(
            "selectedTestContainer"
        ).find_element_by_xpath("//*[text()='waiting to start...']")

    def _select_a_test(self, selenium_driver):
        selenium_driver.find_element_by_xpath('//*[@id="testList"]/tbody/tr').click()

    def _assert_no_test_is_selected(self, selenium_driver):
        assert selenium_driver.find_element_by_id(
            "selectedTestContainer"
        ).find_element_by_xpath("//*[text()='No test selected']")

    def _update_test_result_execution_status(self, sessionmaker_fixture, test_result):
        repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
        test_result.execution_status = ExecutionStatus.RUNNING
        repository.save(test_result)

    def _visit_run_test_page(self, live_server, run, selenium_driver):
        selenium_driver.get(
            f"{live_server.server_url()}/#/projects/{run.project_id}/runs/{run.id}/tests"
        )

    def _assert_first_test_has_icon_with_title(self, selenium_driver, title):
        assert selenium_driver.find_element_by_id("testList").find_element_by_xpath(
            f'//*[@id="testList"]/tbody/tr/td[1]/span[@title="{title}"]'
        )

    def _should_display_test_result(self, selenium_driver, test_result):
        assert (
            selenium_driver.find_element_by_xpath(
                '//*[@id="testList"]/tbody/tr/td[2]'
            ).text
            == test_result.test_identifier.suite_name
        )
        assert (
            selenium_driver.find_element_by_xpath(
                '//*[@id="testList"]/tbody/tr/td[4]'
            ).text
            == test_result.test_identifier.test_name
        )

    def _switch_to_tests_page(self, selenium_driver):
        selenium_driver.find_element_by_id("sidebar").find_element_by_link_text(
            "Tests"
        ).click()

    def _visit_run_overview_page(self, live_server, run, selenium_driver):
        selenium_driver.get(
            f"{live_server.server_url()}/#/projects/{run.project_id}/runs/{run.id}"
        )
