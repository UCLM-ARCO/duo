// -*- mode: c++; coding: utf-8 -*-

#include <Ice/Identity.ice>

module ASD  {

    interface Listener {
	["deprecated:ASD module is deprecated, please use DUO instead."]
	idempotent void adv(Object* prx);

	["deprecated:ASD module is deprecated, please use DUO instead."]
	idempotent void bye(Ice::Identity oid);
  };

};
