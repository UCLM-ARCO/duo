#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

import sys

import dummy_base as base


class BoolGUI(base.GUI):
    pass


class DummyBool(base.Dummy):

    def add_options(self):
        self.arg_parser.add_argument(
            'interface', choices=('R', 'W', 'RW', 'RWA'), type=str,
            help='interface to implement')
        self.arg_parser.add_argument(
            '--init', dest='state', type=bool, help="initial state",
            default=False)

    def do_create_servant(self):
        iface = "IBool.{0}".format(self.args.interface)
        dummyClass = base.MetaDummy(iface)
        return dummyClass(self.args.state)

    def do_create_gui(self):
        return BoolGUI()



if __name__ == "__main__":
    dummy = DummyBool()
    sys.exit(dummy.main(sys.argv, "dummy.cfg"))
