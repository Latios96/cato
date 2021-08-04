from cato.domain.config import RunConfig


class TestConfig:
    def test_correct_suite_count_single_suite(self, config_fixture):
        assert config_fixture.CONFIG.suite_count == 1

    def test_correct_suite_count_multiple_suites(self, config_fixture):
        config_fixture.CONFIG.suites.extend(config_fixture.CONFIG.suites)

        assert config_fixture.CONFIG.suite_count == 2

    def test_correct_test_count_single_test(self, config_fixture):
        assert config_fixture.CONFIG.test_count == 1

    def test_correct_test_count_multiple_tests(self, config_fixture):
        config_fixture.CONFIG.suites[0].tests.extend(
            config_fixture.CONFIG.suites[0].tests
        )

        assert config_fixture.CONFIG.test_count == 2


class TestRunConfig:
    def test_from_config(self, config_fixture):
        run_config = RunConfig.from_config(config_fixture.CONFIG, "test", "output")

        assert run_config == config_fixture.RUN_CONFIG

    def test_to_config(self, config_fixture):
        config = config_fixture.RUN_CONFIG.to_config()

        assert config == config_fixture.CONFIG
