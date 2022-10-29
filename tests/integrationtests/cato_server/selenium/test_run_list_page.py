from selenium.webdriver.common.by import By

from cato_common.domain.branch_name import BranchName
from cato_common.domain.run import Run
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_common.utils.datetime_utils import aware_now_in_utc
from cato_server.domain.run_batch import RunBatch
from tests.integrationtests.cato_server import selenium_test


@selenium_test
class TestRunListPage:
    def test_run_list_pagination(
        self,
        live_server,
        authenticated_selenium_driver,
        project,
        sqlalchemy_run_batch_repository,
        run_batch,
        local_computer_run_information,
        run_batch_identifier,
    ):
        self._insert_many_run_batches(
            project,
            sqlalchemy_run_batch_repository,
            run_batch,
            local_computer_run_information,
            run_batch_identifier,
        )
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
        sqlalchemy_run_batch_repository,
        run_batch,
        local_computer_run_information,
        run_batch_identifier,
    ):
        self._insert_many_run_batches(
            project,
            sqlalchemy_run_batch_repository,
            run_batch,
            local_computer_run_information,
            run_batch_identifier,
        )
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
        sqlalchemy_run_batch_repository,
        run_batch,
        local_computer_run_information,
        run_batch_identifier,
    ):
        self._insert_many_run_batches(
            project,
            sqlalchemy_run_batch_repository,
            run_batch,
            local_computer_run_information,
            run_batch_identifier,
        )

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
        print("SAVED", sqlalchemy_test_result_repository.save(test_result))

    def _assert_first_run_status_icon_has_title(self, selenium_driver, title):
        # //*[@id="runList"]/tbody/tr[1]/td[2]/span
        selenium_driver.wait_until(
            lambda driver: driver.find_element(By.ID, "runList").find_element(
                By.XPATH, f'//*[@id="runList"]/tbody/tr/td[2]/span[@title="{title}"]'
            )
        )

    def _run_25_should_be_on_page(self, selenium_driver):
        selenium_driver.wait_until(
            lambda driver: driver.find_element(By.LINK_TEXT, "#25")
        )

    def _run_50_should_be_on_page(self, selenium_driver):
        assert selenium_driver.find_element(By.LINK_TEXT, "#50")

    def _pagination_buttons_should_be_correctly_enabled(self, selenium_driver):
        selenium_driver.wait_until(
            lambda driver: driver.find_elements(
                By.CSS_SELECTOR, "[aria-label=Previous]"
            )
        )
        previous_button = selenium_driver.find_elements(
            By.CSS_SELECTOR, "[aria-label=Previous]"
        )[0]
        assert not previous_button.is_enabled()
        next_page = selenium_driver.find_elements(
            By.CSS_SELECTOR, "[aria-label='Next Page']"
        )[0]
        assert next_page.is_enabled()
        return next_page

    def _visit_project_page(self, live_server, project, selenium_driver):
        selenium_driver.get(f"{live_server.server_url()}/projects/{project.id}")

    def _insert_many_run_batches(
        self,
        project,
        sqlalchemy_run_batch_repository,
        run_batch,
        local_computer_run_information,
        run_batch_identifier,
    ):
        sqlalchemy_run_batch_repository.insert_many(
            [
                RunBatch(
                    id=0,
                    run_batch_identifier=run_batch_identifier.copy(run_identifier=x),
                    project_id=project.id,
                    created_at=aware_now_in_utc(),
                    runs=[
                        Run(
                            id=0,
                            project_id=project.id,
                            run_batch_id=0,
                            started_at=aware_now_in_utc(),
                            branch_name=BranchName("default")
                            if x > 10
                            else BranchName("dev"),
                            previous_run_id=None,
                            run_information=local_computer_run_information,
                        )
                    ],
                )
                for x in range(50)
            ]
        )

    def _assert_first_run_has_branch_default(self, selenium_driver):
        selenium_driver.wait_until(
            lambda driver: self._select_first_run_branch_name(driver).text == "default"
        )

    def _select_dev_branch(self, selenium_driver):
        selenium_driver.find_element(By.XPATH, "//button[text()='Branch']").click()
        selenium_driver.wait_until(
            lambda driver: driver.find_element(
                By.ID, "branchSelector-open"
            ).find_element(By.XPATH, "//*[text()='dev']")
        )
        selenium_driver.find_element(By.ID, "branchSelector-open").find_element(
            By.XPATH, "//*[text()='dev']"
        ).click()

    def _wait_until_first_run_has_branch_dev(self, selenium_driver):
        selenium_driver.wait_until(
            lambda driver: self._select_first_run_branch_name(driver).text == "dev"
        )

    def _wait_until_url_contains_branch_name(self, selenium_driver):
        selenium_driver.wait_until(lambda driver: "branches=dev" in driver.current_url)

    def _select_first_run_branch_name(self, selenium_driver):
        return selenium_driver.find_element(
            By.XPATH, '//*[@id="runList"]/tbody/tr[1]/td[4]'
        )
