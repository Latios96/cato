import datetime

from cato_common.domain.branch_name import BranchName
from cato_common.domain.run import Run
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_server.storage.sqlalchemy.sqlalchemy_run_repository import (
    SqlAlchemyRunRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)
from tests.integrationtests.conftest import MyChromeDriver


class TestRunListPage:
    def test_run_list_pagination(
        self,
        live_server,
        selenium_driver: MyChromeDriver,
        project,
        sessionmaker_fixture,
    ):
        self._insert_many_runs(project, sessionmaker_fixture)
        self._visit_project_page(live_server, project, selenium_driver)
        next_page = self._pagination_buttons_should_be_correctly_enabled(
            selenium_driver
        )
        self._run_50_should_be_on_page(selenium_driver)

        next_page.click()

        self._run_25_should_be_on_page(selenium_driver)
        selenium_driver.refresh()
        self._run_25_should_be_on_page(selenium_driver)

    def test_run_list_auto_update(
        self,
        live_server,
        selenium_driver: MyChromeDriver,
        project,
        test_result,
        sessionmaker_fixture,
    ):
        self._visit_project_page(live_server, project, selenium_driver)
        self._assert_first_run_status_icon_has_title(selenium_driver, "not started")

        self._update_run_status(sessionmaker_fixture, test_result)

        self._assert_first_run_status_icon_has_title(selenium_driver, "running")

    def _update_run_status(self, sessionmaker_fixture, test_result):
        repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
        test_result.unified_test_status = UnifiedTestStatus.RUNNING
        repository.save(test_result)

    def _assert_first_run_status_icon_has_title(self, selenium_driver, title):
        assert selenium_driver.find_element_by_id("runList").find_element_by_xpath(
            f'//*[@id="runList"]/tbody/tr/td[1]/span[@title="{title}"]'
        )

    def _run_25_should_be_on_page(self, selenium_driver):
        assert selenium_driver.find_element_by_link_text("Run #25")

    def _run_50_should_be_on_page(self, selenium_driver):
        assert selenium_driver.find_element_by_link_text("Run #50")

    def _pagination_buttons_should_be_correctly_enabled(self, selenium_driver):
        previous_button = selenium_driver.find_elements_by_css_selector(
            "[aria-label=Previous]"
        )[0]
        assert not previous_button.is_enabled()
        next_page = selenium_driver.find_elements_by_css_selector(
            "[aria-label='Next Page']"
        )[0]
        assert next_page.is_enabled()
        return next_page

    def _visit_project_page(self, live_server, project, selenium_driver):
        selenium_driver.get(f"{live_server.server_url()}/#/projects/{project.id}")

    def _insert_many_runs(self, project, sessionmaker_fixture):
        repository = SqlAlchemyRunRepository(sessionmaker_fixture)
        repository.insert_many(
            [
                Run(
                    id=0,
                    project_id=project.id,
                    started_at=datetime.datetime.now(),
                    branch_name=BranchName("default"),
                    previous_run_id=None,
                )
                for x in range(50)
            ]
        )
