.DEFAULT_GOAL := help
BIN := wluma-als-emulator
PROJECT := wluma-als-emulator
VERSION := 1.2.0

PREFIX ?= /usr
LIB_DIR = $(DESTDIR)$(PREFIX)/lib
BIN_DIR = $(DESTDIR)$(PREFIX)/bin
SHARE_DIR = $(DESTDIR)$(PREFIX)/share

run: ## Install and test in a virtualenv
	./run.sh

.PHONY: init
init: ## Install requirements
	pip install -r requirements.txt

.PHONY: build
build: ## Build
	python3 setup.py build

.PHONY: install
install: ## Install $(BIN)
	python3 setup.py install  --root="$(DESTDIR)/" --optimize=1 --skip-build

.PHONY: service
service: ## Install the service
	install -Dm644 -t "$(LIB_DIR)/systemd/user" "$(BIN).service"

.PHONY: docs
docs: ## Build and install the documentation
	install -Dm644 -t "$(SHARE_DIR)/licenses/$(BIN)/" LICENSE
	install -Dm644 -t "$(SHARE_DIR)/doc/$(BIN)/" README.* docs/*

.PHONY: dist
dist: ## Make a release with gpg asc
	mkdir -p dist
	git archive -o "dist/$(PROJECT)-$(VERSION).tar.gz" --format tar.gz --prefix "$(PROJECT)-$(VERSION)/" "$(VERSION)"
	gpg --detach-sign --armor "dist/$(PROJECT)-$(VERSION).tar.gz"
	rm -f "dist/$(PROJECT)-$(VERSION).tar.gz"

.PHONY: clean
clean: ## Clean
	rm -rf dist

.PHONY: package
package: docs service install ## Make the packag

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
