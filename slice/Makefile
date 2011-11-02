# -*- mode: makefile, coding: utf-8 -*-

install: clean
	install -vd $(DESTDIR)/usr/share/duo/slice/DUO
	install -m 644 *.ice $(DESTDIR)/usr/share/duo/slice/DUO

.PHONY: clean
clean:
	$(RM) *.o *.h *.cpp *~

