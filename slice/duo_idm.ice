// -*- mode: c++; coding: utf-8 -*-

// slice2x duo_idm.ice -I /usr/share/Ice/slice

#ifndef DUO_IDM_ice
#define DUO_IDM_ice

#include <idm/idm.ice>

module IDM {

    module DUO {

	module IBool {
	    interface W { void set(bool v, IDM::Address oid); };
	};

	module IInt {
	    interface W { void set(int v, IDM::Address oid); };
	};

	module Active {
	    interface R {
		IDM::Address getObserver();
	    };

	    interface W {
		void setObserver(IDM::Address observer);
	    };
	};

	interface Listener {
	    void adv(IDM::Address prx);
	    void bye(IDM::Address oid);
	};
    };
};

#endif
