.PHONY: help
help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  init       to initialize a dev environment"
	@echo "  update     to upload pre-commit hooks and re-install dependencies"
	@echo "  clean      clear tox environments and builds"

.PHONY: init
init:
	pip install -U tox pre-commit
	rm -rf .tox
	pre-commit install

.PHONY: update
update:
	pre-commit autoupdate
	$(MAKE) init

.PHONY: clean
clean:
	rm -rf _build/*
	rm -rf .tox
