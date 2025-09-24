.PHONY: compile publish check fix lint fixlint format mypy deadcode audit test init
args = $(or $(filter-out $@,$(MAKECMDGOALS)), "autogit")
UV := $(shell uv --version 2>/dev/null)
OS := $(shell uname)

run_manual_test:
	rm -fr tmp/*
	auto-git -r repos.txt --clone-to=tmp -m "Update mypy version" ./examples/update_mypy_version.py

check: test lint mypy audit deadcode
fix: format fixlint

.venv:
ifndef UV
	@echo "uv not found. Installing uv.."
	pip install uv
endif
	uv venv -p 3.12
	uv pip sync requirements-dev.txt
	uv pip install -e .[test]

publish: .venv
	rm -fr dist/*
	.venv/bin/hatch build
	.venv/bin/hatch -v publish

lint: .venv
	.venv/bin/ruff check autogit tests

fixlint: .venv
	.venv/bin/ruff check --fix autogit tests --unsafe-fixes
	.venv/bin/deadcode --fix autogit tests

format: .venv
	.venv/bin/ruff format autogit tests

mypy: .venv
	.venv/bin/mypy autogit tests

audit: .venv
	.venv/bin/pip-audit --skip-editable

deadcode: .venv
	.venv/bin/deadcode autogit tests

test: .venv
	.venv/bin/pytest $(TEST_NAME)

sync: .venv
	uv pip sync requirements-dev.txt
	uv pip install -e .[test]

compile:
	uv pip compile -U -q pyproject.toml -o requirements.txt
	uv pip compile -U -q --all-extras pyproject.toml -o requirements-dev.txt

## NOTE: --quiet removes some useful output from commonly used targets.
# Another workaround should be found to suppress init error for target up to date rule.
# MAKEFLAGS += --quiet
init:
	@echo "Initializing ${args}..."
	@if [ $(OS) = "Linux" ]; then\
		git grep -l 'autogit' | xargs sed -i 's/autogit/$(args)/g';\
	fi
	@if [ $(OS) = "Darwin" ]; then\
		git grep -l 'autogit' | xargs sed -i '' -e 's/autogit/$(args)/g';\
	fi
	@sed -i -e 's/[[:digit:]]\+\.[[:digit:]]\+\.[[:digit:]]\+/0.0.1/g' autogit/__init__.py
	@mv autogit $(args)
	@rm -fr .git/ .venv
	@git init -b main .
	@git add .
	@git commit -m "Initial modern $(args) package setup"
	@echo "Finished initializing ${args}. You can now run: \033[0;32m cd ${args} && make check\033[0m"
	@-exit 0

%:
	@:
