from getpass import getpass


class PasswordDidNotMatchException(Exception):
    def __init__(self):
        super(PasswordDidNotMatchException, self).__init__("Passwords did not match.")


class UserCliInput:
    def __init__(self, get_input=input, get_password=getpass):
        self._get_input = get_input
        self._get_password = get_password

    def prompt_username_and_password(self):
        username = self._get_input("Enter username: ")
        username = self._require_not_blank_str(username, "Username")
        password = self._get_password()
        password = self._require_not_blank_str(password, "Password")
        repeated_password = self._get_password(prompt="Repeat password: ")
        repeated_password = self._require_not_blank_str(repeated_password, "Password")

        if not password == repeated_password:
            raise PasswordDidNotMatchException()

        return username, password

    def _require_not_blank_str(self, the_str, name):
        stripped = the_str.strip()
        if not stripped:
            raise ValueError(f"{name} can not be empty or blank.")
        return stripped
