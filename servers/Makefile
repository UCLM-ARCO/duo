# -*- mode: makefile; coding: utf-8 -*-

SHELL=/bin/bash

install: clean
	install -vd $(DESTDIR)/usr/bin/
	install -m 755 duo-* $(DESTDIR)/usr/bin/

	install -vd $(DESTDIR)/etc/duo/
	install -m 644 *.cfg $(DESTDIR)/etc/duo/

.PHONY: clean
clean:
	$(RM) *.pyc *~
