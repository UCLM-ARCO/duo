# -*- mode: makefile, coding: utf-8 -*-

all:

install:
	@echo Installing in $(DESTDIR)
	$(MAKE) -C slice install
	$(MAKE) -C dummies install
	$(MAKE) -C clients install

clean:
	$(MAKE) -C slice clean

