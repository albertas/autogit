from typing import Optional


def flatten_list(list_of_lists: Optional[list[list[str]]]) -> list[str]:
    if not list_of_lists:
        return []
    return [repo for repo_list in list_of_lists for repo in repo_list]
