// -*- mode: c++; coding: utf-8 -*-
//
// slice2x DUO.ice -I /usr/share/Ice/slice

#ifndef DUO_ice
#define DUO_ice

#include <Ice/BuiltinSequences.ice>
#include <Ice/Identity.ice>

module DUO {

  module Pulse {
    interface W { ["freeze:write", "ami"] void set(Ice::Identity oid); };
  };

  module IBool {
    interface R { ["freeze:read", "ami"] idempotent bool get(); };
    interface W { ["freeze:write", "ami"] void set(bool v, Ice::Identity oid); };
  };

  module IByte {
    interface R { ["freeze:read", "ami"] idempotent byte get(); };
    interface W { ["freeze:write", "ami"] void set(byte v, Ice::Identity oid); };
  };

  module IInt {
    interface R { ["freeze:read", "ami"] idempotent int get(); };
    interface W { ["freeze:write", "ami"] void set(int v, Ice::Identity oid); };
  };

  module ILong {
    interface R { ["freeze:read", "ami"] idempotent long get(); };
    interface W { ["freeze:write", "ami"] void set(long v, Ice::Identity oid); };
  };

  module IFloat {
    interface R { ["freeze:read", "ami"] idempotent float get(); };
    interface W { ["freeze:write", "ami"] void set(float v, Ice::Identity oid); };
  };

  module IString {
    interface R { ["freeze:read", "ami"] idempotent string get(); };
    interface W { ["freeze:write", "ami"] void set(string v, Ice::Identity oid); };
  };

  module IByteSeq {
    interface R { ["freeze:read", "ami"] idempotent Ice::ByteSeq get(); };
    interface W { ["freeze:write", "ami"] void set(Ice::ByteSeq v, Ice::Identity oid); };
  };

  module IObject {
    interface R { ["freeze:read", "ami"] idempotent Object* get(); };
    interface W { ["freeze:write", "ami"] void set(Object* v, Ice::Identity oid); };
  };

  module Active {

    interface R {
      ["ami"] Object* getObserver();
    };

    interface W {
      ["ami"] void setObserver(Object* observer);
    };

  };

  dictionary<string, Object*> ObjectPrxDict;

  module Container {
    exception AlreadyExistsException { string key; };
    exception NoSuchKeyException { string key; };

    interface RW;
    interface R { ["freeze:read", "ami"] idempotent ObjectPrxDict list(); };
    interface W {
      // Add and remove external items
      ["freeze:write", "ami"]
	void link(string key, Object* value) throws AlreadyExistsException;

      ["freeze:write", "ami"]
	void unlink(string key) throws NoSuchKeyException;

      // Create new colocated Container children
      ["freeze:write", "ami"]
	Container::RW* create(string key) throws AlreadyExistsException;

      // Destroy *this* object
      ["freeze:write", "ami"]
	void destroy();
    };
    interface RW extends R,W {};
  };


  module Funcional {
    interface Relative {
      void inc(short nsteps);
    };
  };

  interface Component {
    Ice::StringSeq getAllFacets();
  };

  module Composite {

    // Valid operations for byte, int, float, long
    const string MIN = "minimum";  // lowest value
    const string MAX = "maximum";  // highest value
    const string AVG = "average";  // sum(0..n)/n
    const string MED = "median";   // sort(0..n)[n/2]
    const string HEI = "height";   // max-min

    // Valid operations for bool
    const string ANY = "any";      // true if any is true
    const string ALL = "all";      // true if all are true

    // Exceptions
    exception InvalidTypeException { string tid; };
    exception NoSuchObjectException { string oid; };

    // Public Factory to create Composites
    interface Factory {
      Object* create(string scalarType) throws InvalidTypeException;
      void destroy(Object* proxy) throws NoSuchObjectException;
      Ice::StringSeq getAllowedTypes();
    };

    interface R extends DUO::Container::R, DUO::Component{};
    interface W extends DUO::Container::RW, DUO::Component{};
  };

};

#endif
