# -*- mode: python; coding: utf-8 -*-

import gtk
import gobject
import logging
import signal
import argparse

import Ice
import IceStorm


gtk.gdk.threads_init()


def loadSlice(name):
    string = '-I{0} -I. -I../slice --all {1}'
    Ice.loadSlice(string.format(Ice.getSliceDir(), name))


def closeOnSystemExit(mth):
    def _deco(self, *args, **kwargs):
        try:
            return mth(self, *args, **kwargs)
        except SystemExit:
            self.communicator().shutdown()
    _deco.__name__ = mth.__name__
    return _deco


class DummyException(Exception):
    def __init__(self, msg):
        self.message = msg


loadSlice('dummy.ice')
loadSlice('../slice/DUO.ice')

import DUO
import Actor

logging.basicConfig(level=logging.DEBUG,
                    format='DUMMY|%(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',)


class Subject(object):
    observers = []
    state = None

    def set_state(self, val):
        self.state = val
        self.notify()

    def register(self, ob):
        logging.debug("register of '{0}'".format(ob))
        self.observers.append(ob)

    def unregister(self, ob):
        if ob in self.observers:
            logging.debug("unregister of '{0}'".format(ob))
            self.observers.remove(ob)

    def notify(self):
        for ob in self.observers:

            def idle_call():
                try:
                    logging.debug("notify on '{0}'".format(ob))
                    ob.update()
                except Exception, e:
                    logging.error("unexpected behaviour: {0}".format(e))
                    logging.error("removing observer '{0}'".format(ob))
                    self.unregister(ob)

            gobject.idle_add(idle_call)


class Active_I(Subject):

    def __init__(self):
        self.active_observer = None

    def getObserver(self, current=None):
        return self.active_observer

    def setObserver(self, observer, current=None):
        self.observer = observer
        self.reactive = Reactive(self, self.observer)

    def ice_ping(self, current=None):
        logging.info("received a ping()")
        self.notify()


class Dummy_R(Subject):
    def get(self, current=None):
        logging.info("-> get()")

        if self.get_state:
            return self.get_state()

        return self.state


class Dummy_W(Subject):
    def set(self, val, oid, current):
        ic = current.adapter.getCommunicator()
        oid = ic.identityToString(oid)
        logging.info(" -- received set({0}, '{1}')".format(val, oid))

        self.state = val
        self.notify()


class Reactive(object):
    def __init__(self, model, publisher):
        self.model = model
        self.publisher = publisher
        self.model.register(self)

    def update(self):
        self.publisher.set(self.model.state, Ice.Identity())
        logging.info(' -- observer.set({0})'.format(self.model.state))


class DUOCaster(object):
    def cast_proxy(self, proxy):
        module_name = self.ice_id()[2:].replace("::", ".")
        exec "proxy = {0}Prx.uncheckedCast(proxy)".format(module_name)
        return proxy


class MetaDummy(type):
    def __new__(metacls, name):

        def init(obj, val=None, cb=None):
            obj.get_state = cb
            obj.state = val

        duo_ifaces = {'R': Dummy_R, 'W': Dummy_W, 'A': Active_I}
        bases = [duo_ifaces[i] for i in name.split('.')[1]]
        bases.append(DUOCaster)

        base = None
        try:
            if len(name.split('.')[1]) == 1:
                exec "base = DUO.{0}".format(name)
            else:
                exec "base = Actor.{0}".format(name)
        except AttributeError:
            raise DummyException("there is no {0} module!".format(name))

        bases.append(base)
        return type.__new__(
            metacls, name, tuple(bases),
            {'__init__': init, 'base': base})


class Dummy(Ice.Application):

    @closeOnSystemExit
    def run(self, args):
        self.build_parser()
        self.add_options()

        self.args = self.arg_parser.parse_args(args[1:])
        try:
            self.process_args()
        except DummyException, e:
            logging.error("ERROR: {0}".format(e.message))
            self.communicator().shutdown()
            return -1

        self.wait()

    def process_args(self):
        self.build_endpoint_string()
        self.create_adapter()
        self.create_servant()
        self.register_servant()

        self.post_setup_servant()

    def build_endpoint_string(self):
        self.endp = "tcp"
        if not self.args.port is None:
            self.endp += " -p {0}".format(self.args.port)

        if not self.args.host is None:
            self.endp += " -h {0}".format(self.args.host)

    def create_adapter(self):
        try:
            ic = self.communicator()
            self.adapter = ic.createObjectAdapterWithEndpoints(
                "DummyAdapter", self.endp)
        except Ice.SocketException, e:
            raise DummyException(str(e))

        self.adapter.activate()

    def create_servant(self):
        """ To implement on subclass """
        raise NotImplementedError

    def post_setup_servant(self):
        if 'A' in self.args.interface:
            self.setup_servant_as_active()
        if not self.args.suscribe is None:
            self.setup_servant_as_observer()

    def setup_servant_as_active(self):
        topic = self.get_servant_topic()
        publisher = topic.getPublisher()
        publisher = self.servant.cast_proxy(publisher)
        self.servant.setObserver(publisher)

    def get_servant_topic(self):
        topic_mgr = self.get_ice_storm()
        topic_name = Ice.generateUUID()

        try:
            topic = topic_mgr.create(topic_name)
        except IceStorm.TopicExists:
            topic = topic_mgr.retrieve(topic_name)

        logging.info("topic proxy: '{0}'".format(topic))
        return topic

    def get_ice_storm(self):
        ic = self.communicator()
        topic_mgr = ic.propertyToProxy("IceStorm.TopicManager.Proxy")
        topic_mgr = IceStorm.TopicManagerPrx.checkedCast(topic_mgr)
        return topic_mgr

    def setup_servant_as_observer(self):
        ic = self.communicator()
        topic = ic.stringToProxy(self.args.suscribe)
        topic = IceStorm.TopicPrx.checkedCast(topic)
        topic.subscribeAndGetPublisher({}, self.proxy)

    def register_servant(self):
        if not self.args.identity:
            self.proxy = self.adapter.addWithUUID(self.servant)
        else:
            oid = self.communicator().stringToIdentity(self.args.identity)
            self.proxy = self.adapter.add(self.servant, oid)

        logging.info("Proxy used: '{0}'".format(self.proxy))

    def wait(self):
        self.shutdownOnInterrupt()

        signal.signal(signal.SIGINT, gtk.main_quit)
        gtk.main()

        ic = self.communicator()
        ic.shutdown()

    def build_parser(self):
        self.arg_parser = argparse.ArgumentParser(description='Dummy')
        self.arg_parser.add_argument(
            '--id', dest='identity', help='identity of servant')
        self.arg_parser.add_argument(
            '--port', type=int, help='port of object adapter')
        self.arg_parser.add_argument(
            '--host', help='ip where to listen')

        self.arg_parser.add_argument(
            '--suscribe', help='topic on which suscribe servant')

    def add_options(self):
        """ To implement on subclass """
        pass
