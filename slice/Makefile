# -*- mode: makefile, coding: utf-8 -*-

all::

install:: all
	install -vd $(DESTDIR)/usr/share/slice/duo
	install -m 644 *.ice $(DESTDIR)/usr/share/slice/duo

.PHONY: clean
clean::
	$(RM) *.o *.h *.cpp *~ *.so*

# CXX        = g++-4.7
# CXXFLAGS   = -fPIC
# SO_LIBNAME = libduoSlice.so
# SO_TARGET  = $(TARGETS_DIR)/$(SO_LIBNAME)

# include arco/slice.mk

# all:: $(SO_TARGET)
# 	strip $(LIB_FULLNAME)

# install:: all
# 	install -vd $(DESTDIR)/usr/share/slice/duo
# 	install -m 644 *.ice $(DESTDIR)/usr/share/slice/duo
# 	install -m 644 $(SO_TARGET) $(DESTDIR)/usr/lib/

# $(SO_TARGET): $(SLICE_OBJ)
# 	$(CXX) -fPIC -shared -Wl,-soname,$(SO_LIBNAME).35 $^ -o $@

# .PHONY: clean
# clean::
# 	$(RM) *.o *.h *.cpp *~ *.so*
