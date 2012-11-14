# -*- mode: makefile; coding: utf-8 -*-

SHELL=/bin/bash

install: clean
	install -vd $(DESTDIR)/usr/bin/
	install -m 755 duo-client-* $(DESTDIR)/usr/bin/

	install -vd $(DESTDIR)/usr/share/pyshared/duo/clients/
	install -m 644 *.py $(DESTDIR)/usr/share/pyshared/duo/clients/


.PHONY: clean
clean:
	$(RM) *.pyc *~
