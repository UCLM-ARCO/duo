// -*- mode: c++; coding: utf-8 -*-

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
      ["ami"] Object* getCallback();
    };

    interface W {
      ["ami"] void setCallback(Object* callback);
    };

  };
};

#endif
