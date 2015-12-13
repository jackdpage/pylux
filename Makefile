destdir=$(HOME)/.config/
filestoinstall=pylux.conf

all:
	@echo "make options:"
	@echo "      install"
	@echo "      uninstall"

install:
	@install -Cdv "$(destdir)"
	@install -Cv $(filestoinstall) "$(destdir)"
	@install -Cdv "$(HOME)/.openlighting/"
	@cp -rv fixture/ $(HOME)/.openlighting/

uninstall:
	@-rm -rfv "$(HOME)/.openlighting/"
