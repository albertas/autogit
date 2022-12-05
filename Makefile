venv:
	python3.9 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements-dev.txt --use-pep517
	venv/bin/pip install -e .

build:
	venv/bin/hatch build
	venv/bin/hatch publish

flake8:
	venv/bin/flake8 gitmultirepoupdater

mypy:
	venv/bin/mypy gitmultirepoupdater

test:
	venv/bin/pytest $(PYTEST_ME_PLEASE)

check: test flake8 mypy
