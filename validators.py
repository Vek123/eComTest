import re
from datetime import datetime
from typing import Any, List, Type


class Validator(object):
    def __new__(cls, v: Any) -> bool:
        return cls.valid(v)

    @staticmethod
    def valid(v: Any) -> bool:
        raise NotImplementedError()


class PriorityValidator(Validator):
    @staticmethod
    def get_priority() -> int:
        raise NotImplementedError()


class PhoneValidator(PriorityValidator):
    def __new__(cls, phone: str):
        return super().__new__(cls, phone)

    @staticmethod
    def valid(phone: Any) -> bool:
        return re.fullmatch(r"\+7 \d{3} \d{3} \d{2} \d{2}", phone) is not None

    @staticmethod
    def get_priority() -> int:
        return 3


class EmailValidator(PriorityValidator):
    def __new__(cls, email: str):
        return super().__new__(cls, email)

    @staticmethod
    def valid(email: str):
        return re.fullmatch(r".+@.+\..+", email)

    @staticmethod
    def get_priority() -> int:
        return 4


class DateValidator(PriorityValidator):
    date_formats: List[str] = [
        "%d.%m.%Y",
        "%Y-%m-%d",
    ]

    def __new__(cls, date_str: str):
        return cls.valid(date_str)

    @staticmethod
    def valid(date_str: str) -> bool:
        valid_date = False
        for date_format in DateValidator.date_formats:
            try:
                valid_date = datetime.strptime(date_str, date_format) and True
            except ValueError:
                pass

        return valid_date

    @staticmethod
    def get_priority() -> int:
        return 2


def get_validator(field_type: str) -> Type[PriorityValidator]:
    match field_type:
        case "email":
            return EmailValidator
        case "date":
            return DateValidator
        case "phone":
            return PhoneValidator


def get_field_type(field: str) -> str:
    if DateValidator(field):
        return "date"
    elif PhoneValidator(field):
        return "phone"
    elif EmailValidator(field):
        return "email"
    else:
        return "text"
