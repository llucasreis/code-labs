SHELL := /bin/bash

help:	## Show this help.
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'

subscribe: ## run subscribe
	@poetry run python3 src/subscribe.py

publish: ## run publish
	@poetry run python3 src/publish.py

install: ## install
	@poetry install