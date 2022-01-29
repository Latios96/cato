from getpass import getpass

from cato_server.authentication.create_user import CreateUserData
from cato_server.domain.auth.secret_str import SecretStr
from cato_server.domain.auth.username import Username


class PasswordDidNotMatchException(Exception):
    def __init__(self):
        super(PasswordDidNotMatchException, self).__init__("Passwords did not match.")


class UserCliInput:
    def __init__(self, get_input=input, get_password=getpass):
        self._get_input = get_input
        self._get_password = get_password

    def prompt_create_user_data(self) -> CreateUserData:
        username = self._get_input("Enter username: ")
        username = self._require_not_blank_str(username, "Username")
        fullname = self._get_input("Enter user fullname: ")
        fullname = self._require_not_blank_str(fullname, "Full name")
        password = self._get_password()
        password = self._require_not_blank_str(password, "Password")
        repeated_password = self._get_password(prompt="Repeat password: ")
        repeated_password = self._require_not_blank_str(repeated_password, "Password")

        if not password == repeated_password:
            raise PasswordDidNotMatchException()

        return CreateUserData(
            username=Username(username),
            fullname=Username(fullname),
            password=SecretStr(password),
        )

    def _require_not_blank_str(self, the_str: str, name: str) -> str:
        stripped = the_str.strip()
        if not stripped:
            raise ValueError(f"{name} can not be empty or blank.")
        return stripped
