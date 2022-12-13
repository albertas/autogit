#!/usr/bin/env python

import glob
import os
import re
from typing import List, Optional


def get_all_file_paths(directory: Optional[str] = None) -> List[str]:
    """Provides a list of file-paths for every file in a directory (including subdirectories)."""
    if directory is None:
        directory = os.getcwd()

    recursive_directory_path = os.path.abspath(f"{directory.rstrip('/')}/**")
    file_and_dir_paths = glob.glob(recursive_directory_path, recursive=True)
    return [path for path in file_and_dir_paths if not path.endswith("/")]


def replace(filename: str, pattern: str, replace_with: str) -> None:
    """Replaces all patterns found in a file with a `replace_with` fragment."""
    with open(filename, "r") as f:
        content = f.read()

    for mo in list(re.finditer(pattern, content))[::-1]:
        content = content[:mo.start()] + replace_with + content[mo.end():]

    with open(filename, "w") as f:
        f.write(content)


if __name__ == "__main__":
    for filename in get_all_file_paths():
        replace(filename, pattern="mypy==[\\d.]*", replace_with="mypy==0.991")
