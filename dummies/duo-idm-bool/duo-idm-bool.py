#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

import sys
import os
import Ice
import json
import argparse
import thing
from threading import Event
from flask import Flask, render_template, request, Response

pwd = os.path.abspath(os.path.dirname(__file__))
slice_path = os.path.join(pwd, "active-bool.ice")
if not os.path.exists(slice_path):
    slice_path = "/usr/share/duo/dummy/active-bool.ice"

Ice.loadSlice("{} -I/usr/share/slice --all".format(slice_path))
Ice.loadSlice("/usr/share/slice/PropertyService/PropertyService.ice -I/usr/share/slice --all")
import Dummy
import PropertyService
import DUO
import IDM


class IBoolWI(Dummy.ActiveBool):
    def __init__(self, args, router):
        self.args = args
        self.state = args.state == "True"
        self.state_changes = Event()
        self.address = args.address
        self.router = router
        self.observer = None

    def stop(self):
        # wake all waiting threads
        self.state_changes.set()

    def get_state_when_changed(self):
        self.state_changes.wait()
        self.state_changes.clear()
        return self.state

    def set(self, state, source, current=None):
        print(" * Set state to {}".format(state))
        self.state = state
        self.state_changes.set()

        if self.observer is None:
            return

        print(" * Notify observer")
        self.observer.set(state, "")

    def setObserver(self, observer, current):
        if not self.args.enable_observer:
            return

        is_null = True
        for c in observer:
            if c != '\x00':
                is_null = False
                break

        if is_null:
            observer = None
        else:
            observer = self.addressToIdentity(observer)
            ic = current.adapter.getCommunicator()
            self.observer = self.router.ice_identity(ic.stringToIdentity(observer))
            self.observer = self.observer.ice_oneway()
            self.observer = DUO.IDM.IBool.WPrx.uncheckedCast(self.observer)

        print(" * Set observer to {}".format(observer))

    def addressToIdentity(self, address):
        return "".join("{:02x}".format(ord(c)) for c in address)


class WebServer:
    def __init__(self):
        self.ic = Ice.initialize(sys.argv[1:])

    def add_self(fn):
        def deco(*args, **kwargs):
            return fn(WebServer.instance, *args, **kwargs)
        deco.__name__ = fn.__name__
        return deco

    def run(self):
        WebServer.instance = self

        self.parse_args(sys.argv)
        self.create_proxies()
        self.setup_servant()
        self.update_properties()
        self.announce_on_router()
        self.event_loop()

    def event_loop(self):
        self.should_stop = False

        self.app.run(threaded=True, port=self.args.web_server_port)
        self.ic.destroy()
        self.servant.stop()
        self.should_stop = True
        print("\rBye!")

    def announce_on_router(self):
        if self.router is None:
            return

        self.router.adv(self.ic.proxyToString(self.servant_proxy))

    def update_properties(self):
        if self.ps is None:
            return

        print(" * Setting properties on PropertyService")

        tags = ["consumer"]
        if self.args.enable_observer:
            tags.append("producer")

        t_tags = thing.from_(tags)
        t_name = thing.from_(self.args.name)
        t_icon = thing.from_(self.args.icon)

        self.ps.set("{} | tags".format(self.args.address), t_tags)
        self.ps.set("{} | name".format(self.args.address), t_name)
        self.ps.set("{} | icon".format(self.args.address), t_icon)

    def create_proxies(self):
        self.router = self.ic.propertyToProxy("IDM.Router.Proxy")
        if self.router is None:
            print(" * WARN: IDM.Router.Proxy not defined")
        else:
            self.router = IDM.NeighborDiscovery.ListenerPrx.uncheckedCast(self.router)

        self.ps = self.ic.propertyToProxy("PropertyService.Proxy")
        if self.ps is None:
            print(" * WARN: PropertyService.Proxy not defined")
        else:
            self.ps = PropertyService.PropertyServerPrx.uncheckedCast(self.ps)

    def setup_servant(self):
        adapter = self.ic.createObjectAdapterWithEndpoints("Adapter", "tcp")
        adapter.activate()

        self.servant = IBoolWI(self.args, self.router)
        oid = self.ic.stringToIdentity(self.args.address.replace(":", ""))
        self.servant_proxy = adapter.add(self.servant, oid)
        print(" * Proxy ready: '{}'".format(self.servant_proxy))

    def parse_args(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-a", dest="address", default="AA:02", help="IDM Address")
        parser.add_argument(
            "-s", dest="state", default=False, choices=["True", "False"], help="Initial state")
        parser.add_argument(
            '-n', dest="name", default="Dummy", help="Dummy's name")
        parser.add_argument(
            '-i', dest="icon", default="bulb", help="Dummy's icon")
        parser.add_argument(
            '--observer', dest="enable_observer", action="store_true", help="Enable Active.W iface")
        parser.add_argument(
            '--port', dest="web_server_port", default=5000, type=int, help="Web server port")

        self.args, _ = parser.parse_known_args()

    app = Flask(__name__)

    @app.route("/")
    @add_self
    def index(self):
        return render_template("index.html")

    @app.route("/status")
    @add_self
    def get_status(self):
        return json.dumps({
            'state': self.servant.state,
            'address': self.servant.address,
        })

    @app.route("/set")
    @add_self
    def set_state(self):
        new_state = request.args['state'] == "true"
        self.servant.set(new_state, "")
        return ""

    @app.route("/updates")
    @add_self
    def send_updates(self):
        def wait_for_changes():
            while True:
                state = self.servant.get_state_when_changed()
                if self.should_stop:
                    return
                data = {"state": state}
                yield "data: {}\n\n".format(json.dumps(data))

        return Response(wait_for_changes(), mimetype="text/event-stream")


if __name__ == "__main__":
    WebServer().run()
