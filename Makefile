# -*- mode: makefile, coding: utf-8 -*-

all:

install:
	@echo Installing in $(DESTDIR)
	$(MAKE) -C slice install
	$(MAKE) -C dummies install
	$(MAKE) -C clients install
	$(MAKE) -C servers install

arduino-package: ARDUINO_DIST=/tmp/duo-idm/arduino/duo
arduino-package: clean
	$(RM) -rf $(ARDUINO_DIST)

	install -d $(ARDUINO_DIST)
	$(RM) -f duo_idm.h
	slice2c -I /usr/share/slice slice/duo_idm.ice
	install -m 644 duo_idm.h $(ARDUINO_DIST)/

	install -m 644 arduino/keywords.txt $(ARDUINO_DIST)
	install -m 644 arduino/library.properties $(ARDUINO_DIST)

	cd $(ARDUINO_DIST)/..; zip -r arduino-duo-$$(date +%Y%m%d).zip duo
	mv $(ARDUINO_DIST)/../*.zip .


clean:
	$(MAKE) -C slice clean
	$(RM) -f *.zip *~ duo_idm.h
