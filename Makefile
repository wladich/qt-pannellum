define help
Available targets:
	help
	pylint
	flake8
	mypy
	check - all static checks
	venv - create or update venv for development
	clean - clean caches
endef
export help

TOOL_PREFIX=./.venv/bin/

help:
	@echo "$$help"

pylint: venv
	$(TOOL_PREFIX)pylint . --recursive y

black: venv
	$(TOOL_PREFIX)black --diff --check -q .

flake8: venv
	$(TOOL_PREFIX)flake8 .

mypy: venv
	$(TOOL_PREFIX)mypy .

test: venv
	pytest

check: mypy pylint flake8 black test
	@echo All checks passed.

.PHONY: venv
venv:
	uv sync

clean:
	rm -rf ./mypy_cache ./*.egg-info ./.mypy_cache ./__pycache__ ./.pytest_cache ./.venv ./build
