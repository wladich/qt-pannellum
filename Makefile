define help
Available targets:
	help
	mypy
	ruff
	format - properly format all files
	check - all static checks
	venv - create or update venv for development
	clean - clean caches
endef
export help

TOOL_PREFIX=./.venv/bin/

help:
	@echo "$$help"

ruff: venv
	$(TOOL_PREFIX)ruff check .
	$(TOOL_PREFIX)ruff format --check --diff .

format: venv
	$(TOOL_PREFIX)ruff format .


mypy: venv
	$(TOOL_PREFIX)mypy .

test: venv
	pytest

check: mypy ruff
	@echo All checks passed.

.PHONY: venv
venv:
	uv sync

clean: venv
	rm -rf ./mypy_cache ./*.egg-info ./.mypy_cache ./__pycache__ ./.pytest_cache ./.venv ./build
	$(TOOL_PREFIX)ruff clean
