import os

import configparser


class SqlAlchemyConfig:

    def get_connection_str(self):
        ini_path = os.path.join(os.path.dirname(__file__), "connection.ini")
        if os.path.exists(ini_path):
            config = configparser.ConfigParser()
            config.read(ini_path)
            return config.get("connection", "url")
        raise RuntimeError("config.ini not found!")
