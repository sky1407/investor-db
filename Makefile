PY := .venv/bin/python
RUN := PYTHONPATH=src $(PY) -m investordb.cli
AS_OF ?= 2026-10-09

.PHONY: install test lint verify build metrics pipeline serve

install:
	python3 -m venv --without-pip .venv
	python3 -m pip --python $(PY) install -e ".[dev]"

test:
	$(PY) -m pytest -q

lint:
	$(PY) -m ruff check . && $(PY) -m ruff format --check .

verify:
	$(RUN) verify

build:
	$(RUN) build --as-of $(AS_OF)

metrics:
	$(RUN) metrics

pipeline: verify build metrics

serve:
	$(RUN) serve
