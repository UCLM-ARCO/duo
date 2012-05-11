# -*- mode: makefile; coding: utf-8 -*-

SHELL=/bin/bash

install: clean
	install -vd $(DESTDIR)/usr/share/pyshared/duo/clients
	install -m 644 *.py $(DESTDIR)/usr/share/pyshared/duo/clients

	install -vd $(DESTDIR)/usr/share/duo/clients
	install -m 755 *.sh $(DESTDIR)/usr/share/duo/clients

	install -vd $(DESTDIR)/usr/share/duo/config
	install -m 644 *.cfg $(DESTDIR)/usr/share/duo/config

.PHONY: clean
clean:
	$(RM) *.pyc *~


