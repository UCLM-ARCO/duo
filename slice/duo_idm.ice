// -*- mode: c++; coding: utf-8 -*-

// slice2x duo_idm.ice -I /usr/share/Ice/slice

#ifndef DUO_IDM_ice
#define DUO_IDM_ice

#include <idm/idm.ice>

module DUO {

    module IDM {

	module IBool {
	    interface W { void set(bool v, IDM::Address source); };
	};

	module IInt {
	    interface W { void set(int v, IDM::Address source); };
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
	    void adv(IDM::Address obj);
	    void bye(IDM::Address obj);
	};
    };
};

#endif
