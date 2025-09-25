import os
from random import randint
from string import ascii_letters, digits
from urllib.parse import urlparse

from git.cmd import Git

from autogit.constants import ACCESS_TOKEN_VAR_NAMES
from autogit.data_types import RepoState


def remove_suffix(value: str, suffix: str, case_insensitive: bool = True) -> str:
    """Removes suffix from a given string `value` case_insensitive by default."""
    if value.endswith(suffix) or (
        case_insensitive and value.lower().endswith(suffix.lower())
    ):
        return value[: -len(suffix)]
    return value


def get_random_hex() -> str:
    """Returns 8 digit hex code."""
    return hex(randint(2**31 + 1, 2**32))[2:]


def to_kebab_case(value: str) -> str:
    """Converts provided text `value` to a kebab-case name with max length of 100 for a branch name."""
    allowed_chars = ascii_letters + digits + ' -/'
    value = (
        value.replace('.', ' ')
        .replace(',', ' ')
        .replace('\\', ' ')
        .replace(':', ' ')
        .replace(';', ' ')
    )
    ascii_value = ''.join([char for char in value if char in allowed_chars])
    return '-'.join(ascii_value.lower().split())[:100]


def get_access_token(url: str) -> str:
    """Retrieves access token from environment vars suitable for provided URL."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.split('@')[-1].lower()
    access_token_var_name = ACCESS_TOKEN_VAR_NAMES.get(
        domain, ACCESS_TOKEN_VAR_NAMES['DEFAULT']
    )
    return os.getenv(access_token_var_name, '')


def get_domain(url: str) -> str:
    """Returs domain name in lower case."""
    parsed_url = urlparse(url)
    return parsed_url.netloc.split('@')[-1].lower()


def get_repo_owner(url: str) -> str:
    """Parses repository owner from a valid Git url."""
    return url.rsplit('/', 2)[1]


def get_repo_name(url: str) -> str:
    """Parses repository name from a valid Git url."""
    return remove_suffix(url.split('/')[-1], '.git')


def get_default_branch(repo: RepoState):
    g = Git(repo.directory)
    default_branch_name: str = g.execute(
        ['git', 'rev-parse', '--abbrev-ref', 'origin/HEAD']
    )  # type: ignore
    return default_branch_name.split('/', 1)[
        -1
    ]  # removes `origin/` prefix from the result
