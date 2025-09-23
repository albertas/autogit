run_manual_test:
	rm -fr tmp/*
	auto-git -r repos.txt --clone-to=tmp -m "Update mypy version" ./examples/update_mypy_version.py

test: venv
	cd autogit && make test

check: venv
	cd autogit && make check

venv:
	python3.12 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements-dev.txt --use-pep517
	venv/bin/pip install -e .

publish: venv
	rm -fr dist/*
	venv/bin/hatch build
	venv/bin/hatch publish
