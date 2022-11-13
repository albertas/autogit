venv:
	python3.9 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements-dev.txt --use-pep517

install:
	venv/bin/pip install -e .

build:
	venv/bin/hatch build
	venv/bin/hatch publish
