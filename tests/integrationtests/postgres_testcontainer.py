from testcontainers.postgres import PostgresContainer


class PgContainer(PostgresContainer):
    def get_container_host_ip(self):
        return "localhost"
