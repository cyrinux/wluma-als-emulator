.DEFAULT_GOAL := help
BIN := wluma-als-emulator
PROJECT := wluma-als-emulator
VERSION := 1.2.0

PREFIX ?= /usr
LIB_DIR = $(DESTDIR)$(PREFIX)/lib
BIN_DIR = $(DESTDIR)$(PREFIX)/bin
SHARE_DIR = $(DESTDIR)$(PREFIX)/share

run:
	init
	install

init: ## Install requirements
	pip install -r requirements.txt

build: ## Build
	python3 setup.py build

install: ## Install
	python3 setup.py install  --root="$(DESTDIR)/" --optimize=1 --skip-build
	install -Dm644 -t "$(LIB_DIR)/systemd/user" "$(BIN).service"
	install -Dm644 -t "$(SHARE_DIR)/licenses/$(BIN)/" LICENSE
	install -Dm644 -t "$(SHARE_DIR)/doc/$(BIN)/" README.* docs/*

dist: ## Make a release with gpg asc
	mkdir -p dist
	git archive -o "dist/$(PROJECT)-$(VERSION).tar.gz" --format tar.gz --prefix "$(PROJECT)-$(VERSION)/" "$(VERSION)"
	gpg --detach-sign --armor "dist/$(PROJECT)-$(VERSION).tar.gz"
	rm -f "dist/$(PROJECT)-$(VERSION).tar.gz"

clean: ## Clean
	rm -rf dist


help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
