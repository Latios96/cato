from dataclasses import dataclass


@dataclass
class AuthUser:
    id: int
    username: str
    hashed_password: str
