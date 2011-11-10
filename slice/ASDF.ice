// -*- mode: c++; coding: utf-8 -*-

#include <Ice/Identity.ice>

module ASD  {

  interface Listener {
    idempotent void adv(Object* prx);
    idempotent void bye(Ice::Identity oid);
  };

};

