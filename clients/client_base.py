#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

import argparse
import logging
import Ice

logging.getLogger().setLevel(logging.DEBUG)

slice_path = Ice.getSliceDir()
Ice.loadSlice("-I{0} -I.. --all ../slice/DUO.ice".format(slice_path))


def shutdownOnSystemExit(mth):
    def _deco(self, *args, **kwargs):
        try:
            return mth(self, *args, **kwargs)
        except SystemExit:
            self.communicator().shutdown()
    _deco.__name__ = mth.__name__
    return _deco


class ClientException(Exception):
    def __init__(self, msg):
        self.message = msg


class ClientBase(Ice.Application):
    @shutdownOnSystemExit
    def run(self, args):
        self.build_parser()

        try:
            self.args = self.arg_parser.parse_args(args[1:])
            self.create_proxy()
            self.run_actions()

        except ClientException, e:
            logging.error("ERROR: {0}".format(e.message))
            return -1

    def build_parser(self):
        self.arg_parser = argparse.ArgumentParser(description='Client')
        self.arg_parser.add_argument('proxy', help="proxy of remote object")
        self.arg_parser.add_argument('--facet', help="proxy facet to use")

        self.add_options()

    def add_options(self):
        """ To implement in subclass """
        pass

    def create_proxy(self):
        ic = self.communicator()
        self.proxy = ic.stringToProxy(self.args.proxy)

        if self.args.facet:
            self.proxy = self.proxy.ice_facet(self.args.facet)

    def run_actions(self):
        if not self.args.set is None:
            self.do_set()
        if self.args.get:
            self.do_get()
        logging.debug("OK")

    def do_set(self):
        """ To implement in subclass """
        raise NotImplementedError

    def do_get(self):
        """ To implement in subclass """
        raise NotImplementedError
