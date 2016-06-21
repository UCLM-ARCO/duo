// -*- mode: c++; coding: utf-8 -*-

// slice2x duo_idm.ice -I /usr/share/Ice/slice

#ifndef DUO_IDM_ice
#define DUO_IDM_ice

#include <idm/idm.ice>

module DUO {

    module IDM {

	// FIXME: change this to string
	sequence<byte> Address;

	module IBool {
	    interface W { void set(bool v, Address source); };
	};

	module IInt {
	    interface W { void set(int v, Address source); };
	};

	module Active {
	    interface R {
		Address getObserver();
	    };

	    interface W {
		void setObserver(Address observer);
	    };
	};

	interface Listener {
	    void adv(Address obj);
	    void bye(Address obj);
	};
    };
};

#endif
