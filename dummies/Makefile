# -*- mode: makefile; coding: utf-8 -*-

SHELL=/bin/bash

install: clean
	install -vd $(DESTDIR)/usr/share/pyshared/duo/dummies
	install -m 644 *.py $(DESTDIR)/usr/share/pyshared/duo/dummies

	install -vd $(DESTDIR)/usr/share/duo/dummies
	install -m 644 *.ice $(DESTDIR)/usr/share/duo/dummies
	install -m 755 *.sh $(DESTDIR)/usr/share/duo/dummies

	install -vd $(DESTDIR)/usr/share/duo/config
	install -m 644 *.cfg $(DESTDIR)/usr/share/duo/config

.PHONY: clean
clean:
	$(RM) *.pyc *~


