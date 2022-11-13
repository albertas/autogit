venv:
	python3.9 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements-dev.txt --use-pep517

install:
	venv/bin/pip install -e .

build:
	venv/bin/hatch build
	venv/bin/hatch publish

flake8:
	venv/bin/flake8 git_multi_repo_updater

mypy:
	venv/bin/mypy git_multi_repo_updater

test:
	venv/bin/pytest $(PYTEST_ME_PLEASE)

check: flake8 mypy test
