// -*- mode: c++; coding: utf-8 -*-

#include "DUO.ice"
// #include "DUO/ASDF.ice"
// #include "DUO/Services.ice"

module DummyDUO {

//   module Pulse {
//     interface WA extends DUO::Pulse::W, DUO::Active::R {};
//   };

    module IBool {
	interface RW extends DUO::IBool::R, DUO::IBool::W {};
	interface RWA extends RW, DUO::Active::R, DUO::Active::W {};
//     interface RWP extends RW, ASD::PropHldr {};
//     interface RWPS extends RWP, ASD::Search {};
//     interface RWPSA extends RWPS, DUO::Active::R, DUO::Active::W {};
   };

    module IByte {
	interface RW extends DUO::IByte::R, DUO::IByte::W {};
	interface RWA extends RW, DUO::Active::R, DUO::Active::W {};
//     interface RWP extends RW, ASD::PropHldr {};
//     interface RWPS extends RWP, ASD::Search {};
//     interface RWPSA extends RWPS, DUO::Active::R, DUO::Active::W {};
   };

//   module IInt {
//     interface RA extends DUO::IInt::R, DUO::Active::R, DUO::Active::W {};
//     interface RW extends DUO::IInt::R, DUO::IInt::W {};
//     interface RWP extends RW, ASD::PropHldr {};
//     interface RWPS extends RWP, ASD::Search {};
//     interface RWPSA extends RWPS, DUO::Active::R, DUO::Active::W {};
//   };

//   module IFloat {
//     interface RA extends DUO::IFloat::R, DUO::Active::R, DUO::Active::W {};
//     interface RW extends DUO::IFloat::R, DUO::IFloat::W {};
//     interface RWP extends RW, ASD::PropHldr {};
//     interface RWPS extends RWP, ASD::Search {};
//     interface RWPSA extends RWPS, DUO::Active::R, DUO::Active::W {};
//     interface RPSA extends DUO::IFloat::R, ASD::PropHldr, ASD::Search, DUO::Active::R {};
//   };

  module IString {
//     interface RA extends DUO::IString::R, DUO::Active::R, DUO::Active::W {};
    interface RW extends DUO::IString::R, DUO::IString::W {};
//     interface RWP extends RW, ASD::PropHldr {};
//     interface RWPS extends RWP, ASD::Search {};
//     interface RWPSA extends RWPS, DUO::Active::R, DUO::Active::W {};
  };

//   module IByteSeq {
//     interface RP extends DUO::IBool::R, ASD::PropHldr {};
//     interface RW extends DUO::IBool::R, DUO::IBool::W {};
//     interface RWP extends RW, ASD::PropHldr {};
//     interface RWPS extends RWP, ASD::Search {};
//     interface RWPSA extends RWPS, DUO::Active::R, DUO::Active::W {};
//   };

//   module Container {
//     interface R extends Service::Context, DUO::Container::R {};
//     interface W extends Service::Context, DUO::Container::W {};
//     interface RW extends Service::Context, DUO::Container::RW {};
//     interface RWP extends RW, ASD::PropHldr {};
//     interface RWPS extends RWP, ASD::Search {};
//     interface RWPSA extends RWPS, DUO::Active::R, DUO::Active::W {};
//   };

};
