.PHONY: bufgen
bufgen:
	buf generate buf.build/lekkodev/sdk
	sed -i'.bak' -e 's/^from lekko.client.v1beta1/from ./' lekko_client/gen/lekko/client/v1beta1/*.py
	rm lekko_client/gen/lekko/client/v1beta1/*.bak
