from enum import Enum


class AccountType(str, Enum):
    USER = "user"
    MERCHANT = "merchant"
