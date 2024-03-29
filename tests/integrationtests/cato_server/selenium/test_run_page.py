import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.unified_test_status import UnifiedTestStatus
from tests.integrationtests.cato_server import selenium_test


@selenium_test
class TestRunOverviewPage:
    def test_navigate_back_to_project_page(
        self, live_server, authenticated_selenium_driver, run
    ):
        self._visit_run_overview_page(live_server, run, authenticated_selenium_driver)
        project_page_link = authenticated_selenium_driver.find_element(
            By.LINK_TEXT, "Back to Project"
        )

        project_page_link.click()

        assert authenticated_selenium_driver.find_element(By.LINK_TEXT, "#1")

    def test_overview_page_should_auto_update(
        self,
        live_server,
        authenticated_selenium_driver,
        run,
        test_result,
        sqlalchemy_test_result_repository,
    ):
        self._visit_run_overview_page(live_server, run, authenticated_selenium_driver)
        self._verify_failed_tests_count_to_be(authenticated_selenium_driver, 0)
        self._fail_test(sqlalchemy_test_result_repository, test_result)
        self._verify_failed_tests_count_to_be(authenticated_selenium_driver, 0)

    def _verify_failed_tests_count_to_be(self, selenium_driver, count):
        selenium_driver.wait_until(
            lambda driver: driver.find_element(
                By.XPATH,
                f'//*[@id="runSummary failed tests-value" and text()="{count}"]',
            )
        )

    def _fail_test(self, sqlalchemy_test_result_repository, test_result):
        test_result.status = ResultStatus.FAILED
        sqlalchemy_test_result_repository.save(test_result)

    def _visit_run_overview_page(self, live_server, run, selenium_driver):
        selenium_driver.get(
            f"{live_server.server_url()}/projects/{run.project_id}/runs/{run.id}"
        )


class TestRunTestPage:
    def test_navigation_to_test_page_should_work(
        self, live_server, authenticated_selenium_driver, run, test_result
    ):
        self._visit_run_overview_page(live_server, run, authenticated_selenium_driver)

        self._switch_to_tests_page(authenticated_selenium_driver)

        self._should_display_test_result(authenticated_selenium_driver, test_result)

    def test_auto_update_test_page_should_work(
        self,
        live_server,
        authenticated_selenium_driver,
        run,
        test_result,
        sqlalchemy_test_result_repository,
    ):
        self._visit_run_test_page(live_server, run, authenticated_selenium_driver)

        self._assert_first_test_has_icon_with_title(
            authenticated_selenium_driver, "not started"
        )

        self._update_test_result_status(sqlalchemy_test_result_repository, test_result)

        self._assert_first_test_has_icon_with_title(
            authenticated_selenium_driver, "running"
        )

    def test_selecting_a_test_should_display_the_test(
        self, live_server, authenticated_selenium_driver, run, test_result
    ):
        self._visit_run_test_page(live_server, run, authenticated_selenium_driver)
        self._assert_no_test_is_selected(authenticated_selenium_driver)
        self._select_a_test(authenticated_selenium_driver, test_result)
        self._assert_test_is_selected(authenticated_selenium_driver)

    def test_selecting_a_test_should_display_should_survive_refresh(
        self, live_server, authenticated_selenium_driver, run, test_result
    ):
        self._visit_run_test_page(live_server, run, authenticated_selenium_driver)
        self._assert_no_test_is_selected(authenticated_selenium_driver)
        self._select_a_test(authenticated_selenium_driver, test_result)
        self._assert_test_is_selected(authenticated_selenium_driver)
        authenticated_selenium_driver.refresh()
        self._assert_test_is_selected(authenticated_selenium_driver)

    def test_changing_the_test_selection_should_work(
        self,
        live_server,
        authenticated_selenium_driver,
        run,
        test_result,
        saving_test_result_factory,
    ):
        other_test = saving_test_result_factory(
            suite_result_id=test_result.suite_result_id,
            unified_test_status=UnifiedTestStatus.RUNNING,
        )
        self._visit_run_test_page(live_server, run, authenticated_selenium_driver)
        self._select_a_test(authenticated_selenium_driver, test_result)
        self._assert_test_is_selected(authenticated_selenium_driver)
        self._select_a_test(authenticated_selenium_driver, other_test)
        self._assert_other_test_is_selected(authenticated_selenium_driver)

    def test_editing_the_tests_comparison_settings_should_work(
        self,
        live_server,
        authenticated_selenium_driver,
        run,
        saving_test_result_factory,
        suite_result,
        stored_image,
    ):
        test_result = saving_test_result_factory(
            suite_result_id=suite_result.id,
            unified_test_status=UnifiedTestStatus.SUCCESS,
            image_output=stored_image.id,
            reference_image=stored_image.id,
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=0.8
            ),
        )
        self._visit_run_test_page(live_server, run, authenticated_selenium_driver)
        self._select_a_test(authenticated_selenium_driver, test_result)
        self._edit_tests_threshold(authenticated_selenium_driver)
        self._test_should_be_updated(authenticated_selenium_driver)

    def test_editing_the_tests_reference_image_should_work(
        self,
        live_server,
        authenticated_selenium_driver,
        run,
        saving_test_result_factory,
        suite_result,
        stored_image,
    ):
        test_result = saving_test_result_factory(
            suite_result_id=suite_result.id,
            unified_test_status=UnifiedTestStatus.FAILED,
            message="Reference image <not found> does not exist!",
            image_output=stored_image.id,
            reference_image=None,
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=0.8
            ),
        )
        self._visit_run_test_page(live_server, run, authenticated_selenium_driver)
        self._select_a_test(authenticated_selenium_driver, test_result)
        self._update_tests_reference_image(authenticated_selenium_driver)
        self._test_reference_image_should_be_updated(authenticated_selenium_driver)

    def _assert_other_test_is_selected(self, selenium_driver):
        assert selenium_driver.find_element(
            By.ID, "selectedTestContainer"
        ).find_element(By.XPATH, "//*[text()='started: ']")

    def _assert_test_is_selected(self, selenium_driver):
        assert selenium_driver.wait_until(
            lambda driver: driver.find_element(
                By.ID, "selectedTestContainer"
            ).find_element(By.XPATH, "//*[text()='waiting to start...']")
        )

    def _select_a_test(self, selenium_driver, test_result):
        selenium_driver.wait_until(
            lambda driver: driver.find_element(By.ID, f"test-{test_result.id}").click(),
            5,
        )

    def _assert_no_test_is_selected(self, selenium_driver):
        assert selenium_driver.find_element(
            By.ID, "selectedTestContainer"
        ).find_element(By.XPATH, "//*[text()='No test selected']")

    def _update_test_result_status(
        self, sqlalchemy_test_result_repository, test_result
    ):
        test_result.unified_test_status = UnifiedTestStatus.RUNNING
        sqlalchemy_test_result_repository.save(test_result)

    def _visit_run_test_page(self, live_server, run, selenium_driver):
        selenium_driver.get(
            f"{live_server.server_url()}/projects/{run.project_id}/runs/{run.id}/tests"
        )

    def _assert_first_test_has_icon_with_title(self, selenium_driver, title):
        selenium_driver.wait_until(
            lambda driver: driver.find_element(By.ID, "testList").find_element(
                By.XPATH, f'//*[@id="testList"]/tbody/tr/td[1]/span[@title="{title}"]'
            ),
            20,
        )

    def _should_display_test_result(self, selenium_driver, test_result):
        selenium_driver.wait_until(
            lambda driver: driver.find_element(
                By.XPATH, '//*[@id="testList"]/tbody/tr/td[3]'
            ).text
            == test_result.test_identifier.suite_name,
            5,
        )

        selenium_driver.wait_until(
            lambda driver: driver.find_element(
                By.XPATH, '//*[@id="testList"]/tbody/tr/td[5]'
            ).text
            == test_result.test_identifier.test_name,
            5,
        )

    def _switch_to_tests_page(self, selenium_driver):
        selenium_driver.find_element(By.ID, "sidebar").find_element(
            By.LINK_TEXT, "Tests"
        ).click()

    def _visit_run_overview_page(self, live_server, run, selenium_driver):
        selenium_driver.get(
            f"{live_server.server_url()}/projects/{run.project_id}/runs/{run.id}"
        )

    def _edit_tests_threshold(self, selenium_driver):
        selenium_driver.find_element(By.XPATH, '//button[text()="Edit"]').click()
        selenium_driver.find_element(
            By.XPATH, '//input[@data-testid="edit-comparison-settings-threshold"]'
        ).clear()
        selenium_driver.find_element(
            By.XPATH, '//input[@data-testid="edit-comparison-settings-threshold"]'
        ).send_keys("5.000")
        selenium_driver.find_element(By.XPATH, '//button[text()="OK"]').click()

    def _test_should_be_updated(self, selenium_driver):
        selenium_driver.wait_until(
            expected_conditions.presence_of_element_located(
                (
                    By.XPATH,
                    "//span[text()='Images are not equal! SSIM score was 1.000, max threshold is 5.000']",
                )
            )
        )

    def _update_tests_reference_image(self, selenium_driver):
        selenium_driver.find_element(
            By.XPATH, '//button[text()="Update Reference Image"]'
        ).click()

    def _test_reference_image_should_be_updated(self, selenium_driver):
        selenium_driver.wait_until_not(
            expected_conditions.presence_of_element_located(
                (
                    By.XPATH,
                    "//span[text()='Reference image <not found> does not exist!']",
                )
            )
        )


class TestRunSuitePage:
    def test_navigation_to_suite_page_should_work(
        self,
        live_server,
        authenticated_selenium_driver,
        run,
        test_result,
        suite_result,
    ):
        self._visit_run_overview_page(live_server, run, authenticated_selenium_driver)

        self._switch_to_suites_page(authenticated_selenium_driver)

        self._should_display_suite_result(authenticated_selenium_driver, suite_result)

    def test_expand_suite_should_work(
        self,
        live_server,
        authenticated_selenium_driver,
        run,
        test_result,
        suite_result,
    ):
        self._visit_run_suite_page(live_server, run, authenticated_selenium_driver)
        assert not self._current_url_contains_suite_id(
            authenticated_selenium_driver, suite_result.id
        )

        self._click_expand_icon(authenticated_selenium_driver, suite_result)

        self._should_display_test_result(
            authenticated_selenium_driver, suite_result, test_result
        )
        assert self._current_url_contains_suite_id(
            authenticated_selenium_driver, suite_result.id
        )

    def test_expand_suite_should_survive_page_update(
        self,
        live_server,
        authenticated_selenium_driver,
        run,
        test_result,
        suite_result,
    ):
        self._visit_run_suite_page(live_server, run, authenticated_selenium_driver)
        assert not self._current_url_contains_suite_id(
            authenticated_selenium_driver, suite_result.id
        )

        self._click_expand_icon(authenticated_selenium_driver, suite_result)
        self._should_display_test_result(
            authenticated_selenium_driver, suite_result, test_result
        )

        authenticated_selenium_driver.refresh()

        self._should_display_test_result(
            authenticated_selenium_driver, suite_result, test_result
        )

    def test_select_test_from_suite_should_display_the_test(
        self,
        live_server,
        authenticated_selenium_driver,
        run,
        test_result,
        suite_result,
    ):
        self._visit_run_suite_page(live_server, run, authenticated_selenium_driver)
        assert not self._current_url_contains_test_id(
            authenticated_selenium_driver, test_result.id
        )

        self._click_expand_icon(authenticated_selenium_driver, suite_result)
        self._select_test(authenticated_selenium_driver, suite_result, test_result)

        self._should_display_test_result_right(
            authenticated_selenium_driver, suite_result, test_result
        )

        assert self._current_url_contains_test_id(
            authenticated_selenium_driver, test_result.id
        )

    def test_select_test_from_suite_should_survive_refresh(
        self,
        live_server,
        authenticated_selenium_driver,
        run,
        test_result,
        suite_result,
    ):
        self._visit_run_suite_page(live_server, run, authenticated_selenium_driver)
        assert not self._current_url_contains_test_id(
            authenticated_selenium_driver, test_result.id
        )

        self._click_expand_icon(authenticated_selenium_driver, suite_result)
        self._select_test(authenticated_selenium_driver, suite_result, test_result)
        authenticated_selenium_driver.refresh()

        self._should_display_test_result_right(
            authenticated_selenium_driver, suite_result, test_result
        )

        assert self._current_url_contains_test_id(
            authenticated_selenium_driver, test_result.id
        )

    def test_suite_should_auto_update(
        self,
        live_server,
        authenticated_selenium_driver,
        run,
        suite_result,
        test_result,
        sqlalchemy_test_result_repository,
    ):
        self._visit_run_suite_page(live_server, run, authenticated_selenium_driver)

        self._assert_first_suite_status_icon_has_title(
            authenticated_selenium_driver, suite_result, "not started"
        )

        self._update_run_status(sqlalchemy_test_result_repository, test_result)

        self._assert_first_suite_status_icon_has_title(
            authenticated_selenium_driver, suite_result, "running"
        )

    def test_expanded_suite_should_auto_update(
        self,
        live_server,
        authenticated_selenium_driver,
        run,
        suite_result,
        test_result,
        sqlalchemy_test_result_repository,
    ):
        self._visit_run_suite_page(live_server, run, authenticated_selenium_driver)
        self._click_expand_icon(authenticated_selenium_driver, suite_result)

        self._assert_first_test_status_icon_has_title(
            authenticated_selenium_driver, "not started"
        )

        self._update_run_status(sqlalchemy_test_result_repository, test_result)

        self._assert_first_test_status_icon_has_title(
            authenticated_selenium_driver, "running"
        )

    def _select_test(self, selenium_driver, suite_result, test_result):
        selenium_driver.find_element(
            By.ID, f"suite-{suite_result.id}-test-{test_result.id}"
        ).click()

    def _should_display_test_result(self, selenium_driver, suite_result, test_result):
        assert (
            selenium_driver.find_element(
                By.XPATH,
                f'//*[@id="suite-{suite_result.id}-test-{test_result.id}"]/span[3]',
            ).text
            == test_result.test_name
        )

    def _current_url_contains_suite_id(self, selenium_driver, suite_id):
        return f"selectedSuite={suite_id}" in selenium_driver.current_url

    def _current_url_contains_test_id(self, selenium_driver, test_id):
        return f"selectedTest={test_id}" in selenium_driver.current_url

    def _visit_run_overview_page(self, live_server, run, selenium_driver):
        selenium_driver.get(
            f"{live_server.server_url()}/projects/{run.project_id}/runs/{run.id}"
        )

    def _switch_to_suites_page(self, selenium_driver):
        selenium_driver.find_element(By.ID, "sidebar").find_element(
            By.LINK_TEXT, "Suites"
        ).click()

    def _should_display_suite_result(self, selenium_driver, suite_result):
        assert (
            selenium_driver.find_element(
                By.XPATH, f'//*[@id="suiteListEntry{suite_result.id}"]/span[3]'
            ).text
            == suite_result.suite_name
        )

    def _visit_run_suite_page(self, live_server, run, selenium_driver):
        selenium_driver.get(
            f"{live_server.server_url()}/projects/{run.project_id}/runs/{run.id}/suites"
        )

    def _click_expand_icon(self, selenium_driver, suite_result):
        selenium_driver.find_element(By.ID, f"toggleSuite{suite_result.id}Icon").click()

    def _should_display_test_result_right(
        self, selenium_driver, suite_result, test_result
    ):
        assert (
            selenium_driver.find_element(
                By.XPATH,
                f'//*[@id="suite-{suite_result.id}-test-{test_result.id}"]/span[3]',
            ).text
            == test_result.test_name
        )

    def _assert_first_suite_status_icon_has_title(
        self, selenium_driver, suite_result, title
    ):
        selenium_driver.wait_until(
            lambda driver: driver.find_element(
                By.XPATH, f'//*[@id="suiteListEntry{suite_result.id}"]/span[2]/span'
            ).get_attribute("title")
            == title
        )

    def _assert_first_test_status_icon_has_title(self, selenium_driver, title):
        selenium_driver.wait_until(
            lambda driver: driver.find_element(By.ID, "suiteList").find_element(
                By.XPATH, f'//*[@id="suite-1-test-1"]/span[1]/span[@title="{title}"]'
            )
        )

    def _update_run_status(self, sqlalchemy_test_result_repository, test_result):
        test_result.unified_test_status = UnifiedTestStatus.RUNNING
        sqlalchemy_test_result_repository.save(test_result)


@pytest.mark.parametrize("page", ["suite", "test"])
def test_filtering_suites_and_tests_should_work(
    authenticated_selenium_driver, live_server, run, test_result, page
):
    authenticated_selenium_driver.get(
        f"{live_server.server_url()}/projects/{run.project_id}/runs/{run.id}/{page}s"
    )
    authenticated_selenium_driver.find_element(
        By.XPATH, f'//*[@id="{page}List"]//*[@title="not started"]'
    )

    authenticated_selenium_driver.find_element(By.ID, "Not Started").click()

    authenticated_selenium_driver.find_element(
        By.XPATH, f'//*[@id="{page}List"]//*[@title="not started"]'
    )

    authenticated_selenium_driver.find_element(By.ID, "Failed").click()

    authenticated_selenium_driver.wait_until_not(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f'//*[@id="{page}List"]//*[@title="not started"]')
        ),
        timeout=3,
    )
    authenticated_selenium_driver.find_element(
        By.XPATH, f'//*[@id="{page}List"]//*[text()="No {page}s"]'
    )


@pytest.mark.parametrize("page", ["suite", "test"])
def test_filtering_suites_and_tests_should_read_from_url(
    authenticated_selenium_driver, live_server, run, test_result, page
):
    authenticated_selenium_driver.get(
        f"{live_server.server_url()}/projects/{run.project_id}/runs/{run.id}/{page}s?statusFilter=FAILED"
    )

    authenticated_selenium_driver.wait_until_not(
        expected_conditions.presence_of_element_located(
            (By.XPATH, f'//*[@id="{page}List"]//*[@title="not started"]')
        ),
        timeout=3,
    )
    authenticated_selenium_driver.find_element(
        By.XPATH, f'//*[@id="{page}List"]//*[text()="No {page}s"]'
    )
