import json
from dataclasses import dataclass

import pytest
import requests
from keycloak import KeycloakAdmin
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_container_is_ready


class KeycloakContainer(DockerContainer):
    def __init__(
        self,
        image="quay.io/keycloak/keycloak:17.0.0",
        port=8080,
        keycloak_admin="admin",
        keycloak_admin_username="admin",
    ):
        super(KeycloakContainer, self).__init__(
            image,
        )
        self.port_to_expose = port
        self.with_exposed_ports(self.port_to_expose)
        self._keycloak_admin = keycloak_admin
        self._keycloak_admin_username = keycloak_admin_username

    def _configure(self):
        self.with_env("KEYCLOAK_ADMIN", self._keycloak_admin)
        self.with_env("KEYCLOAK_ADMIN_PASSWORD", self._keycloak_admin_username)
        self.with_command("start-dev")

    @wait_container_is_ready()
    def _connect(self):
        requests.get(self.get_connection_url())

    def get_connection_url(self):
        port = self.get_exposed_port(self.port_to_expose)
        return f"http://localhost:{port}"

    def start(self):
        self._configure()
        super().start()
        self._connect()
        return self


@dataclass
class KeycloakFixture:
    keycloak_container: KeycloakContainer
    keycloak_admin: KeycloakAdmin


@pytest.fixture
def keycloak():
    with KeycloakContainer() as kcc:
        keycloak_admin = KeycloakAdmin(
            server_url=f"{kcc.get_connection_url()}/",
            username="admin",
            password="admin",
            realm_name="master",
        )
        yield KeycloakFixture(keycloak_container=kcc, keycloak_admin=keycloak_admin)


@pytest.fixture
def keycloak_with_realm(keycloak: KeycloakFixture, test_resource_provider):
    with open(test_resource_provider.resource_by_name("realm-export.json")) as f:
        keycloak.keycloak_admin.create_realm(json.load(f))

    keycloak.keycloak_admin.realm_name = "cato-dev"

    yield keycloak


@pytest.fixture
def keycloak_with_realm_and_users(keycloak_with_realm: KeycloakFixture):
    user_id = keycloak_with_realm.keycloak_admin.create_user(
        {
            "enabled": True,
            "username": "test",
            "emailVerified": True,
            "email": "test@foo.com",
            "firstName": "Jan",
            "lastName": "Honsbrok",  # todo other name
        }
    )
    keycloak_with_realm.keycloak_admin.set_user_password(
        user_id, "password", temporary=False
    )

    yield keycloak_with_realm
