from cato_common.domain.branch_name import BranchName
from cato_common.domain.run import Run
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_common.utils.datetime_utils import aware_now_in_utc
from tests.integrationtests.cato_server import selenium_test


@selenium_test
class TestRunListPage:
    def test_run_list_pagination(
        self,
        live_server,
        authenticated_selenium_driver,
        project,
        sqlalchemy_run_repository,
    ):
        self._insert_many_runs(project, sqlalchemy_run_repository)
        self._visit_project_page(live_server, project, authenticated_selenium_driver)
        next_page = self._pagination_buttons_should_be_correctly_enabled(
            authenticated_selenium_driver
        )
        self._run_50_should_be_on_page(authenticated_selenium_driver)

        next_page.click()

        self._run_25_should_be_on_page(authenticated_selenium_driver)
        authenticated_selenium_driver.refresh()
        self._run_25_should_be_on_page(authenticated_selenium_driver)

    def test_run_list_auto_update(
        self,
        live_server,
        authenticated_selenium_driver,
        project,
        test_result,
        sqlalchemy_test_result_repository,
    ):
        self._visit_project_page(live_server, project, authenticated_selenium_driver)
        self._assert_first_run_status_icon_has_title(
            authenticated_selenium_driver, "not started"
        )

        self._update_run_status(sqlalchemy_test_result_repository, test_result)

        self._assert_first_run_status_icon_has_title(
            authenticated_selenium_driver, "running"
        )

    def test_run_list_filter_by_branch(
        self,
        project,
        live_server,
        authenticated_selenium_driver,
        sqlalchemy_run_repository,
    ):
        self._insert_many_runs(project, sqlalchemy_run_repository)
        self._visit_project_page(live_server, project, authenticated_selenium_driver)

        self._assert_first_run_has_branch_default(authenticated_selenium_driver)
        self._select_dev_branch(authenticated_selenium_driver)
        self._wait_until_first_run_has_branch_dev(authenticated_selenium_driver)
        self._wait_until_url_contains_branch_name(authenticated_selenium_driver)

    def test_run_list_filter_by_branch_should_survive_page_refresh(
        self,
        project,
        live_server,
        authenticated_selenium_driver,
        sqlalchemy_run_repository,
    ):
        self._insert_many_runs(project, sqlalchemy_run_repository)

        self._visit_project_page_with_branch_filter_dev(
            live_server, project, authenticated_selenium_driver
        )

        self._wait_until_first_run_has_branch_dev(authenticated_selenium_driver)

    def _visit_project_page_with_branch_filter_dev(
        self, live_server, project, selenium_driver
    ):
        selenium_driver.get(
            f"{live_server.server_url()}/projects/{project.id}?branches=dev"
        )

    def _update_run_status(self, sqlalchemy_test_result_repository, test_result):
        test_result.unified_test_status = UnifiedTestStatus.RUNNING
        sqlalchemy_test_result_repository.save(test_result)

    def _assert_first_run_status_icon_has_title(self, selenium_driver, title):
        selenium_driver.wait_until(
            lambda driver: driver.find_element_by_id("runList").find_element_by_xpath(
                f'//*[@id="runList"]/tbody/tr/td[1]/span[@title="{title}"]'
            )
        )

    def _run_25_should_be_on_page(self, selenium_driver):
        selenium_driver.wait_until(
            lambda driver: driver.find_element_by_link_text("Run #25")
        )

    def _run_50_should_be_on_page(self, selenium_driver):
        assert selenium_driver.find_element_by_link_text("Run #50")

    def _pagination_buttons_should_be_correctly_enabled(self, selenium_driver):
        selenium_driver.wait_until(
            lambda driver: driver.find_elements_by_css_selector("[aria-label=Previous]")
        )
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
        selenium_driver.get(f"{live_server.server_url()}/projects/{project.id}")

    def _insert_many_runs(self, project, sqlalchemy_run_repository):
        sqlalchemy_run_repository.insert_many(
            [
                Run(
                    id=0,
                    project_id=project.id,
                    started_at=aware_now_in_utc(),
                    branch_name=BranchName("default") if x > 10 else BranchName("dev"),
                    previous_run_id=None,
                )
                for x in range(50)
            ]
        )

    def _assert_first_run_has_branch_default(self, selenium_driver):
        selenium_driver.wait_until(
            lambda driver: self._select_first_run_branch_name(driver).text == "default"
        )

    def _select_dev_branch(self, selenium_driver):
        selenium_driver.find_element_by_xpath("//button[text()='Branch']").click()
        selenium_driver.wait_until(
            lambda driver: driver.find_element_by_id(
                "branchSelector-open"
            ).find_element_by_xpath("//*[text()='dev']")
        )
        selenium_driver.find_element_by_id("branchSelector-open").find_element_by_xpath(
            "//*[text()='dev']"
        ).click()

    def _wait_until_first_run_has_branch_dev(self, selenium_driver):
        selenium_driver.wait_until(
            lambda driver: self._select_first_run_branch_name(driver).text == "dev"
        )

    def _wait_until_url_contains_branch_name(self, selenium_driver):
        selenium_driver.wait_until(lambda driver: "branches=dev" in driver.current_url)

    def _select_first_run_branch_name(self, selenium_driver):
        return selenium_driver.find_element_by_xpath(
            '//*[@id="runList"]/tbody/tr[1]/td[3]'
        )
