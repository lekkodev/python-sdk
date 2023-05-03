PYTHON?=python

.PHONY: venv
venv: venv/bin/touchfile

venv/bin/touchfile: pyproject.toml
	@test -d venv || ${PYTHON} -m venv venv
	. venv/bin/activate; pip install .[dev]
	@touch venv/bin/touchfile

.PHONY: test
test: venv
	venv/bin/tox -p auto

.PHONY: lint
lint: venv
	venv/bin/tox -e lint

.PHONY: typecheck
typecheck: venv
	venv/bin/tox -e typecheck

.PHONY: fmt
fmt: venv
	venv/bin/tox -e fmt

.PHONY: bufgen
bufgen:
	buf generate buf.build/lekkodev/sdk
	sed -i'.bak' -e 's/^from lekko.client.v1beta1/from ./' lekko_client/gen/lekko/client/v1beta1/*.py
	rm lekko_client/gen/lekko/client/v1beta1/*.bak
