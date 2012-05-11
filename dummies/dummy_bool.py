#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

import sys

import dummy_base as base


class DummyBool(base.Dummy):

    def add_options(self):
        self.arg_parser.add_argument(
            'interface', choices=('R', 'W', 'RW', 'RWA'), type=str,
            help='interface to implement')
        self.arg_parser.add_argument(
            '--init', dest='state', type=bool, help="initial state",
            default=False)

    def create_servant(self):
        iface = "IBool.{0}".format(self.args.interface)
        dummyClass = base.MetaDummy(iface)
        self.servant = dummyClass(self.args.state)


if __name__ == "__main__":
    dummy = DummyBool()
    sys.exit(dummy.main(sys.argv, "dummy.cfg"))
