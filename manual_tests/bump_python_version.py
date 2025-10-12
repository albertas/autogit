#! /usr/bin/python3

with open('pyproject.toml') as f:
    updated_content = f.read().replace(
        'python_version = "3.13"',
        'python_version = "3.14"'
    )
with open('pyproject.toml', 'w') as f:
    f.write(updated_content)
