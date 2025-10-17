1: venv312
	venv312/bin/autogit -r repos.txt add_hello_to_readme.py

2: venv312
	venv312/bin/autogit -r repos.txt -m "Bump Python version 2" bump_python_version.py


venv312:
	python3.12 -m venv venv312
	venv312/bin/pip install ../.

clean:
	rm -fr venv312
