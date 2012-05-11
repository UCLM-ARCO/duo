# -*- mode: makefile; coding: utf-8 -*-

SHELL=/bin/bash

install: clean
	install -vd $(DESTDIR)/usr/share/pyshared/duo/dummies
	install -m 644 *.py $(DESTDIR)/usr/share/pyshared/duo/dummies

	install -vd $(DESTDIR)/usr/share/duo/dummies
	install -m 644 *.{ice,cfg} $(DESTDIR)/usr/share/duo/dummies
	install -m 755 *.sh $(DESTDIR)/usr/share/duo/dummies

.PHONY: clean
clean:
	$(RM) *.pyc *~


