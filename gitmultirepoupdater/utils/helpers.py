from typing import Optional
from random import randint
from string import ascii_letters, digits


def flatten_list(list_of_lists: Optional[list[list[str]]]) -> list[str]:
    if not list_of_lists:
        return []
    return [repo for repo_list in list_of_lists for repo in repo_list]


def remove_suffix(value: str, suffix: str, case_insensitive: bool = True) -> str:
    if (
        value.endswith(suffix)
        or (case_insensitive and value.lower().endswith(suffix.lower()))
    ):
        return value[:-len(suffix)]
    return value


def get_random_hex() -> str:
    """Returns 8 digit hex code."""
    return hex(randint(2**31 + 1, 2**32))[2:]


def to_kebab_case(value: str) -> str:
    allowed_chars = ascii_letters + digits + " -/"
    value = value.replace(".", " ").replace(",", " ").replace("\\", " ").replace(":", " ").replace(";", " ")
    ascii_value = "".join([l for l in value if l in allowed_chars])
    return "-".join(ascii_value.lower().split())[:100]
