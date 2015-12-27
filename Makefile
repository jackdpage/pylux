destdir=$(HOME)/.pylux/
filestoinstall=pylux.conf genlux.cls

all:
	@echo "make options:"
	@echo "      install"
	@echo "      uninstall"

install:
	@install -Cdv "$(destdir)"
	@install -Cv $(filestoinstall) "$(destdir)"
	@cp -rv fixture/ $(HOME)/.pylux/

uninstall:
	@-rm -rfv "$(HOME)/.pylux/"
