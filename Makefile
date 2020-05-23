BIN := wluma-als-emulator
PROJECT := wluma-als-emulator
VERSION := 1.0.0

PREFIX ?= /usr
LIB_DIR = $(DESTDIR)$(PREFIX)/lib
BIN_DIR = $(DESTDIR)$(PREFIX)/bin
SHARE_DIR = $(DESTDIR)$(PREFIX)/share

.PHONY: run
run: $(BIN)

.PHONY: clean
clean:
	rm -rf dist

.PHONY: install
install:
	install -Dm755 -t "$(BIN_DIR)/" $(BIN)
	install -Dm644 -t "$(LIB_DIR)/systemd/user" "$(BIN).service"
	install -Dm644 -t "$(SHARE_DIR)/licenses/$(BIN)/" LICENSE
	install -Dm644 -t "$(SHARE_DIR)/doc/$(BIN)/" README.md

.PHONY: dist
dist:
	mkdir -p dist
	git archive -o "dist/$(PROJECT)-$(VERSION).tar.gz" --format tar.gz --prefix "$(PROJECT)-$(VERSION)/" "$(VERSION)"
	gpg --detach-sign --armor "dist/$(PROJECT)-$(VERSION).tar.gz"
	rm -f "dist/$(PROJECT)-$(VERSION).tar.gz"
