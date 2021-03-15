def test_correct_suite_count_single_suite(config_fixture):
    assert config_fixture.CONFIG.suite_count == 1


def test_correct_suite_count_multiple_suites(config_fixture):
    config_fixture.CONFIG.test_suites.extend(config_fixture.CONFIG.test_suites)

    assert config_fixture.CONFIG.suite_count == 2


def test_correct_test_count_single_test(config_fixture):
    assert config_fixture.CONFIG.test_count == 1


def test_correct_test_count_multiple_tests(config_fixture):
    config_fixture.CONFIG.test_suites[0].tests.extend(
        config_fixture.CONFIG.test_suites[0].tests
    )

    assert config_fixture.CONFIG.test_count == 2
