// -*- mode: c++; coding: utf-8 -*-

// slice2x DUO.ice -I /usr/share/Ice/slice

#ifndef DUO_ice
#define DUO_ice

#include <Ice/BuiltinSequences.ice>
#include <Ice/Identity.ice>

module DUO {

    interface Async { void asyncGet(Object* sink); };

    module Pulse {
	interface W { void set(Ice::Identity oid); };
    };

    module IBool {
	interface R { idempotent bool get(); };
	interface W { void set(bool v, Ice::Identity oid); };
    };

    module IByte {
	interface R { idempotent byte get(); };
	interface W { void set(byte v, Ice::Identity oid); };
    };

    module IInt {
	interface R { idempotent int get(); };
	interface W { void set(int v, Ice::Identity oid); };
    };

    module ILong {
	interface R { idempotent long get(); };
	interface W { void set(long v, Ice::Identity oid); };
    };

    module IFloat {
	interface R { idempotent float get(); };
	interface W { void set(float v, Ice::Identity oid); };
    };

    module IString {
	interface R { idempotent string get(); };
	interface W { void set(string v, Ice::Identity oid); };
    };

    module IByteSeq {
	interface R { idempotent Ice::ByteSeq get(); };
	interface W { void set(Ice::ByteSeq v, Ice::Identity oid); };
    };

    module IObject {
	interface R { idempotent Object* get(); };
	interface W { void set(Object* v, Ice::Identity oid); };
    };

    module Active {
	interface R {
	    Object* getObserver();
	};

	interface W {
	    void setObserver(Object* observer);
	};
    };

    dictionary<string, Object*> ObjectPrxDict;

    module Container {
	exception AlreadyExistsException { string key; };
	exception NoSuchKeyException { string key; };

	interface RW;
	interface R { idempotent ObjectPrxDict list(); };
	interface W {
	    // Add and remove external items
	    void link(string key, Object* value) throws AlreadyExistsException;

	    void unlink(string key) throws NoSuchKeyException;

	    // Create new colocated Container children
	    Container::RW* create(string key) throws AlreadyExistsException;

	    // Destroy *this* object
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

    // Device advertisement
    interface DeviceObserver {
	void adv(string deviceId, string deviceType, Object* device);
	void bye(string deviceId);
    };

    // Service advertisement
    interface Listener {
	idempotent void adv(Object* prx);
	idempotent void bye(Ice::Identity oid);
    };

};

#endif
