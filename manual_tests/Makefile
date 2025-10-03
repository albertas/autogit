run: venv312
	venv312/bin/autogit --clone-to=tmp -r repos.txt hello.py
	# venv312/bin/autogit --clone-to=tmp -r repos.txt hello.py
	# venv312/bin/autogit -r repos.txt hello.py

update:
	venv312/bin/pip uninstall autogit
	venv312/bin/pip install autogit

venv312:
	python3.12 -m venv venv312
	venv312/bin/pip install autogit
