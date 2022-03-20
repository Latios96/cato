from typing import Optional

from cato_common.domain.auth.email import Email
from cato_common.mappers.abstract_value_mapper import AbstractValueMapper


class EmailValueMapper(AbstractValueMapper[Email, str]):
    def map_from(self, email_str: Optional[str]) -> Optional[Email]:
        if not email_str:
            return None
        return Email(email_str)

    def map_to(self, email: Email) -> str:
        return str(email)
