# -*- mode: makefile, coding: utf-8 -*-

CXX=g++-4.6
include arco/slice.mk

install:: clean
	install -vd $(DESTDIR)/usr/share/slice/duo
	install -m 644 *.ice $(DESTDIR)/usr/share/slice/duo

.PHONY: clean
clean::
	$(RM) *.o *.h *.cpp *~
