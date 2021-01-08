import os


class BaseCliCommand(object):
    def _config_path(self, path):
        if not path:
            path = os.getcwd()
        path = os.path.abspath(path)
        if os.path.isdir(path):
            path = os.path.join(path, "cato.json")
        return path
