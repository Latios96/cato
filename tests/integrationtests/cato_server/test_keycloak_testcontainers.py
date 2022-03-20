from tests.integrationtests.cato_server import testcontainers_test
from tests.integrationtests.cato_server.conftest import KeycloakFixture


@testcontainers_test
def test_keycloak_testcontainer(keycloak_with_realm_and_users: KeycloakFixture):
    users = keycloak_with_realm_and_users.keycloak_admin.get_users()
    assert users[0]["username"] == "test"
