import os

import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SqlAlchemyConfig:
    def get_connection_str(self):
        ini_path = os.path.join(os.path.dirname(__file__), "config.ini")
        if os.path.exists(ini_path):
            config = configparser.ConfigParser()
            config.read(ini_path)
            return config.get("connection", "url")
        raise RuntimeError("config.ini not found!")

    def get_engine(self):
        return create_engine(self.get_connection_str(), pool_size=10, max_overflow=20)

    def get_session_maker(self):
        return sessionmaker(bind=self.get_engine())

    def get_file_storage_path(self):
        ini_path = os.path.join(os.path.dirname(__file__), "config.ini")
        if os.path.exists(ini_path):
            config = configparser.ConfigParser()
            config.read(ini_path)
            return config.get("connection", "file_storage")
        raise RuntimeError("config.ini not found!")
