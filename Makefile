PYTHON?=python3

.PHONY: venv
venv: venv/bin/touchfile

venv/bin/touchfile: pyproject.toml
	@test -d venv || ${PYTHON} -m venv venv
	. venv/bin/activate; pip install .[dev]
	@touch venv/bin/touchfile

.PHONY: test
test: venv
	PYTHONPATH=. venv/bin/tox -p auto
	venv/bin/tox -e report

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
	buf generate buf.build/lekkodev/sdk --type lekko.client.v1beta1
	buf generate buf.build/lekkodev/cli --type lekko.rules.v1beta3 --type lekko.feature.v1beta1 --type lekko.backend.v1beta1
	grep -rl "from lekko.\|import lekko.\|type: lekko.\|lekko." ./lekko_client/gen --include \*.py --include \*.pyi | xargs sed -i'.bak' -E -e 's/([ \[])lekko\./\1lekko_client.gen.lekko./g'
	rm -f lekko_client/gen/lekko/client/v1beta1/*.bak
	rm -f lekko_client/gen/lekko/feature/v1beta1/*.bak
	rm -f lekko_client/gen/lekko/rules/v1beta3/*.bak
	rm -f lekko_client/gen/lekko/backend/v1beta1/*.bak
