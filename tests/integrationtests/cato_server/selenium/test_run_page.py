from cato.domain.test_status import TestStatus
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)
from tests.integrationtests.conftest import MyChromeDriver


class TestRunPage:
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
