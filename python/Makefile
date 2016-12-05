# -*- mode: makefile; coding: utf-8 -*-

SHELL=/bin/bash

install: clean
	install -vd $(DESTDIR)/usr/share/pyshared/duo/
	install -m 644 *.py $(DESTDIR)/usr/share/pyshared/duo/


.PHONY: clean
clean:
	$(RM) *.pyc *~
