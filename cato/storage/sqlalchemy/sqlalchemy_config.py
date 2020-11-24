import os

import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SqlAlchemyConfig:
    def get_connection_str(self):
        ini_path = os.path.join(os.path.dirname(__file__), "connection.ini")
        if os.path.exists(ini_path):
            config = configparser.ConfigParser()
            config.read(ini_path)
            return config.get("connection", "url")
        raise RuntimeError("config.ini not found!")

    def get_engine(self):
        return create_engine(self.get_connection_str())

    def get_session_maker(self):
        return sessionmaker(bind=self.get_engine())
