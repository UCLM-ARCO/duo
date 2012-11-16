# -*- mode: makefile; coding: utf-8 -*-

SHELL=/bin/bash

install: clean
	install -vd $(DESTDIR)/usr/share/pyshared/duo/dummies/
	install -m 644 *.py $(DESTDIR)/usr/share/pyshared/duo/dummies/
	touch $(DESTDIR)/usr/share/pyshared/duo/__init__.py

	install -vd $(DESTDIR)/usr/share/duo/dummy/pixmaps/
	install -m 644 *.{ice,glade} $(DESTDIR)/usr/share/duo/dummy/
	install -m 644 pixmaps/* $(DESTDIR)/usr/share/duo/dummy/pixmaps/

	install -vd $(DESTDIR)/usr/bin/
	install -m 755 duo-dummy-* $(DESTDIR)/usr/bin/

.PHONY: clean
clean:
	$(RM) *.pyc *~
