# -*- mode: makefile; coding: utf-8 -*-

SHELL=/bin/bash

install: DST = $(DESTDIR)/usr/lib/python3/dist-packages/duo/
install: clean
	install -vd $(DST)
	install -m 644 *.py $(DST)


.PHONY: clean
clean:
	$(RM) *.pyc *~
