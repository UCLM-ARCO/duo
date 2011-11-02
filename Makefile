# -*- mode: makefile, coding: utf-8 -*-

all:

install:
	@echo Installing in $(DESTDIR)
	$(MAKE) -C slice install

clean:
	$(MAKE) -C slice clean

