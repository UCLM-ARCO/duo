# -*- mode: python; coding: utf-8 -*-

# import gtk
# import gobject
# import sys
import logging
# import signal
import argparse

# import IceStorm
import Ice


# gtk.gdk.threads_init()
logging.getLogger().setLevel(logging.DEBUG)


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

# loadSlice('dummy.ice')
# loadSlice('%s/ASDF.ice' % HESPERIA_SLICE)
# loadSlice('%s/PropertyService.ice' % HESPERIA_SLICE)
# loadSlice('%s/PropertyType.ice' % HESPERIA_SLICE)

# import DUO, ASD, PropertyService, Actor

# logging.basicConfig(level=logging.DEBUG,
#                     format='DUMMY|%(levelname)s: %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',)


# def identityToString(oid):
#     cat = oid.category
#     if cat: cat+= '/'
#     return cat+oid.name


# class TextAreaStream(file):
#     def __init__(self, textview):
#         self.textview = textview
#         self.buffer = textview.get_buffer()


#     def write(self, msg):
#         gobject.idle_add(self.buffer.insert_at_cursor, msg)
#         gobject.idle_add(self.textview.scroll_mark_onscreen, self.buffer.get_insert())


#     def flush(self):
#         pass



# # Access to glade objects transparently
# class GladeWrapper:
#     def __init__(self, fname, widget=None):
#         self.__glade = gtk.glade.XML(fname, widget)
#         self.__glade.signal_autoconnect(self)
# #        self.get_widget = self._glade.get_widget

#     def __getattr__(self, name):
#         try:
#             return self.__dict__[name]
#         except KeyError, e:
#             if name.startswith("wg_"):
#                 ret = self.__glade.get_widget(name[3:])
#                 if ret:
#                     self.__dict__[name] = ret
#                     return ret
#             raise AttributeError, "%s: %s" % (str(self.__class__), e)



# #FIXME: que esto sea un hbox y así se evita la siguiente función
# class dummyColorBand(gtk.DrawingArea):
#     def __init__(self):
#         gtk.DrawingArea.__init__(self)
#         self.connect("expose-event", self.expose)
#         self.x = 20
#         self.y = 20


#     def expose(self, widget, event):
#         ctx = widget.window.cairo_create()
#         ctx.rectangle(event.area.x, event.area.y,
#                       event.area.width, event.area.height)
#         ctx.clip()
#         self.draw(ctx)
#         return False


#     def draw(self, ctx):
#         width = self.get_allocation().width
#         n = width/self.x

#         for i in range(0,n+2):
#             ctx.move_to(i*self.x, 0)
#             ctx.line_to(i*self.x+self.x, 0)
#             ctx.line_to(i*self.x, self.y)
#             ctx.line_to(i*self.x-self.x, self.y)
#             ctx.close_path()
#             if i%2: ctx.set_source_rgb(1, 0.83, 0.16)
#             else:   ctx.set_source_rgb(0, 0, 0)
#             ctx.fill_preserve()
#             ctx.set_source_rgb(0, 0, 0)
#             ctx.stroke()


#     def get_size(self):
#         return (self.x, self.y)



# def create_dummy_band(hbox):
#     band = dummyColorBand()
#     hbox.set_size_request(-1, band.get_size()[1])
#     hbox.pack_start(band)
#     band.show()



# class GUI(GladeWrapper):
#     gui = None
#     def __init__(self, model, iface, proxy):
#         self.model = model
#         self.model.register(self)

#         GladeWrapper.__init__(self, "dummyBase.glade")

#         create_dummy_band(self.wg_hbox_top)
#         create_dummy_band(self.wg_hbox_bottom)

#         self.wg_label_type.set_text(iface)
#         self.wg_entry_proxy.set_text('%s' % proxy)

#         if isinstance(model, Active_I):
#             self.wg_expander_active.show()
#             self.wg_entry_callback.set_text('%s' % model.publisher)
#             self.wg_entry_topic.set_text('%s' % model.own_topic)
#             self.wg_expander_active.show()

#         assert isinstance(self.gui, gtk.Widget),\
#             "Debes definir un atributo 'gui' en la clase derivada."
#         self.gui.unparent()
#         self.wg_frame_container.add(self.gui)

#         self.textArea_handler = logging.StreamHandler(TextAreaStream(self.wg_textview_log))
#         logging.getLogger().addHandler(self.textArea_handler)

#         # Property service enabled
#         if isinstance(self.model, PropHldrI):
#             self.wg_label_properties.hide()
#             self.wg_box_properties.show_all()

#             cell = gtk.CellRendererText()
#             tvcolumn1 = gtk.TreeViewColumn("key", cell)
#             tvcolumn1.add_attribute(cell, "text", 0)
#             tvcolumn2 = gtk.TreeViewColumn("value", cell)
#             tvcolumn2.add_attribute(cell, "text", 1)

#             self.wg_treeview_properties.append_column(tvcolumn1)
#             self.wg_treeview_properties.append_column(tvcolumn2)
#             self.wg_treeview_properties.set_model(self.model.properties)

#         self.update()


#     def update(self):
#         if isinstance(self.model, Active_I):
#             self.wg_entry_callback.set_text('%s' % self.model.publisher)
#             self.wg_entry_topic.set_text('%s' % self.model.own_topic)


#     def refresh_cb_topic(self):
#         self.wg_entry_callback.set_text('%s' % model.publisher)
#         self.wg_entry_topic.set_text('%s' % model.own_topic)


#     def error_message(self, msg):
#         logging.error(msg)
#         self.wg_dialog_error_label.set_text(msg)
#         self.wg_dialog_error.run()
#         self.wg_dialog_error.hide()


#     # Gui callbacks
#     def on_window_delete_event(self, event, data):
#         logging.getLogger().removeHandler(self.textArea_handler)
#         gtk.main_quit()


#     def on_button_prop_add_clicked(self, widget):
#         key_entry = self.wg_dialog_add_entry_key
#         value_entry = self.wg_dialog_add_entry_value

#         def __on_activate(widget):
#             self.wg_dialog_add.response(gtk.RESPONSE_OK)

#         def __clean():
#             key_entry.set_text("")
#             key_entry.grab_focus()
#             value_entry.set_text("")

#         key_entry.connect("activate", __on_activate)
#         value_entry.connect("activate", __on_activate)

#         key_entry.grab_focus()
#         ret = self.wg_dialog_add.run()
#         while (True):
#             if ret == 0: # Clean pressed
#                 __clean()

#             elif ret == gtk.RESPONSE_OK:
#                 key = key_entry.get_text()
#                 value = value_entry.get_text()
#                 if key and value:
#                     self.model.setp({key:ASD.strValue(value)})
#                     __clean()
#                     break
#                 else:
#                     self.error_message("There can't be empty fields!")
#                     if not key: key_entry.grab_focus()
#                     else: value_entry.grab_focus()

#             elif ret == gtk.RESPONSE_CANCEL or ret == gtk.RESPONSE_DELETE_EVENT:
#                 __clean()
#                 break

#             ret = self.wg_dialog_add.run()

#         self.wg_dialog_add.hide()


#     def on_button_prop_del_clicked(self, widget):
#         path = self.wg_treeview_properties.get_cursor()[0]
#         if path:
#             key = self.wg_treeview_properties.get_model()[path][0]
#             self.model.delp([key])
#         else:
#             logging.info("No item selected!")


#     def on_button_prop_edit_clicked(self, widget):
#         path = self.wg_treeview_properties.get_cursor()[0]
#         if path:
#             prop = self.wg_treeview_properties.get_model()[path]
#             self.wg_dialog_add_entry_key.set_text(prop[0])
#             self.wg_dialog_add_entry_value.set_text(prop[1])

#             self.wg_button_prop_add.clicked()
#         else:
#             logging.info("No item selected!")


class Subject(object):
    observers = []
    state = None

    def set_state(self, val):
        self.state = val
        self.notify()

    def register(self, ob):
        self.observers.append(ob)

    def unregister(self, ob):
        if ob in self.observers:
            self.observers.remove(ob)

    def notify(self):
        for ob in self.observers:
            gobject.idle_add(ob.update)


# class PropHldrI(object):

#     properties = gtk.ListStore(str, str, object)

#     def getp(self, current=None):
#         if not hasattr(self, 'propPrx'):
#             ic = current.adapter.getCommunicator()
#             props = ic.getProperties()
#             endpoint = props.getProperty("PropertyService.Endpoints")
#             oid = ic.identityToString(current.id)

#             nexo = " -t:" if not "@" in endpoint else " "
#             prx = ic.stringToProxy(oid+nexo+endpoint)

#             self.propPrx = PropertyService.PropertySetDefPrx.uncheckedCast(prx)

#         return self.propPrx



# class Search_I:
#     def __adv(self, pub):
#         try:
#             # wait a random time
#             import random, time
#             time.sleep(random.randrange(0, 2000)/1000.0)

#             pub.adv(self.prx, None)
#             logging.info("lookup: adv() sent")

#         except Ice.Exception, e:
#             logging.error(str(e))


#     # cb is a ListenerPrx
#     def lookup(self, cb, tid, query, current=None):
#         logging.info("-> lookup('%s')" % tid)
#         ids = self.prx.ice_ids()

#         # send ADV only if tid is correct...
#         if tid and not tid in ids:
#             logging.info(" ... '%s' not in ids" % tid)
#             return

#         # and, if there is no query
#         if not query:
#             return self.__adv(cb)

#         # if there is query, but not P, don't send adv
#         if not "::ASD::PropHldr" in ids:
#             return

#         # match properties and, if so, send adv
#         try:
#             not_empty, props = self.getp(current).getProperties(query.keys())
#             for key,p in query.items():
#                 try:
#                     if p.value != props[key].value:
#                         return

#                 # value not in props
#                 except KeyError, e:
#                     return

#                 props.pop(key)
#                 query.pop(key)

#             if not props and not query:
#                 return self.__adv(cb)

#         except Ice.Exception, e:
#             logging.error("Cannot connect to PropertyService: %s" % e)


#     # tengo que preguntar cual es el objetivo de esta función
#     def discover(self, current=None):
#         pass



# class Active_I(Subject):
#     '''this object send current state to active topic when it changes
#     and is state observer'''

#     own_topic = None
#     publisher = None
#     reactive_observer = None

#     def ice_ping(self, current=None):
#         logging.info("-> ping()")
#         self.notify()

#     # methods from DUO::Active::R
#     def getCb(self, current=None):
#         return self.publisher

#     def getTopic(self, current=None):
#         return self.own_topic

#     # methods from DUO::Active::W
#     def setCbTopic(self, pub, topic, current=None):
#         if self.publisher: self.unregister(self.publisher)
#         if self.reactive_observer: self.unregister(self.reactive_observer)
#         self.publisher = pub

#         if self.publisher:
#             ids = self.prx.ice_ids()
#             iface = [id.split('::')[2] for id in ids if "DUO" in id and not "Active" in id][0]
#             exec "prx_class = DUO.%s.WPrx" % iface
#             active_pub = prx_class.uncheckedCast(pub)
#             logging.info("Active pub: %s" % active_pub)
#             self.reactive_observer = Reactive(self, iface, active_pub)

#         # ¿se debe eliminar el topic anterior?
#         if self.own_topic:
#             self.own_topic.destroy()

#         self.own_topic = topic
#         self.notify()


class Dummy_R(Subject):
    def get(self, current=None):
        logging.info("-> get()")

        if self.get_state:
            return self.get_state()

        return self.state


class Dummy_W(Subject):
    def set(self, val, oid, current=None):
        self.state = val
        self.notify()

        ic = current.adapter.getCommunicator()
        logging.info("-> set(%s, %s)" % (val, ic.identityToString(oid)))



# class IceMethods(object):

#     __fake_ids = tuple() # add this ids to 'legal' ids
#     __fake     = False
#     __dummy_id = True    # should dummy id be displayed

#    def ice_ids(self, current=None):
#         if self.__fake:
#             ids = self.__fake_ids + ('::Ice::Object',)

#         else:
#             ids = self.base.ice_ids(self, current) + self.__fake_ids

#         if not self.__dummy_id:
#             ids = [iface for iface in ids if ((not "Actor" in iface) or (iface in self.__fake_ids))]

#         return ids

#     def ice_isA(self, name, current=None):
#         return name in self.ice_ids(current)

#     def ice_id(self, current=None):
#         if not self.__dummy_id:
#             return self.ice_ids(current)[0]
#         else:
#             return self.base.ice_id(self, current)

#     # internal setup
#     def _add_fake_ids(self, ifaces):
#         for iface in ifaces:
#             if not iface in self.__fake_ids:
#                 self.__fake_ids += (iface,)

#     def _set_fake_ids(self, ifaces):
#         self.__fake = True
#         self._add_fake_ids(ifaces)

#     def _del_dummy_id(self):
#         self.__dummy_id = False



# metaclase
class MetaDummy(type):
    def __new__(metacls, name):

        def init(obj, val=None, cb=None):
            obj.get_state = cb
            obj.state = val

        duo_ifaces = {'R': Dummy_R, 'W': Dummy_W}
#                       'P':PropHldrI, 'S':Search_I, 'A':Active_I}

        bases = [duo_ifaces[i] for i in name.split('.')[1]]
#       bases += (IceMethods,)

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
            metacls, name, tuple(bases), {'__init__': init, 'base': base})


# # Ejemplo de lo que hace la metaclase (ficticio)
# # c = MetaDummy('IByte.RW')
# #
# # class RW(Actor.IByte.RW, Dummy_R, Dummy_W):
# #    def __init__(self, val): self.state = val


# class Reactive:
#     'this object send current state to active publisher when it changes'
#     def __init__(self, model, id, publisher):
#         self.model = model
#         self.publisher = publisher
#         self.model.register(self)
#         self.id = id


#     @property
#     def __set_args(self):
#         if self.id == "Pulse":
#             return (Ice.Identity(),)

#         else:
#             if self.model.get_state:
#                 state = self.model.get_state()
#             else:
#                 state = self.model.state

#             return (state, Ice.Identity())


#     def update(self):
#         try:
#             self.publisher.set(*self.__set_args)
#             logging.info('<- set(%s)' % self.model.state)

#         except Ice.ObjectNotExistException:
#             self.model.observers.remove(self)
#             logging.debug('Deleting %s from observers' %(self.publisher))



class Dummy(Ice.Application):

#     def __init__(self, opts):
#         self.opts = opts

#         self.__no_announce = False
#         if "--no-announce" in opts:
#             self.__no_announce = True


#     def delete(self):
#         if self.announce_topic:
#             self.send_bye()

#         if hasattr(self.servant, "own_topic") and self.servant.own_topic:
#             logging.info("Deleting own active topic.")
#             self.servant.own_topic.destroy()

#         # Si lo añadimos, hay que quitarlo
#         if "--container-prx" in self.opts:
#             __base = self.communicator().stringToProxy(self.opts["--container-prx"])
#             try:
#                 if __base.ice_isA("::DUO::Container::RW"):
#                     __cprx = DUO.Container.RWPrx.checkedCast(__base)
#                     __key = identityToString(self.prx.ice_getIdentity())
#                     __cprx.unlink(__key)
#                     logging.info("Object removed from '%s'" % __cprx)
#             except Ice.Exception, e:
#                 logging.warning("Couldn't contact with container to remove myself!\n%s" % e)

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

#         if "--hide-dummy-iface" in self.opts:
#             self.servant._del_dummy_id()

#         # something like "::Module::Interface"
#         if "--add-fake-ifaces" in self.opts:
#             ifaces = self.opts['--add-fake-ifaces'].split(',')
#             self.servant._add_fake_ids(ifaces)

#         if "--fake-ifaces" in self.opts:
#             ifaces = self.opts['--fake-ifaces'].split(',')
#             self.servant._set_fake_ids(ifaces)

#         # Si necesitamos añadirlo en algún sitio...
#         if "--container-prx" in self.opts:
#             __base = self.communicator().stringToProxy(self.opts["--container-prx"])
#             try:
#                 if __base.ice_isA("::DUO::Container::RW"):
#                     __cprx = DUO.Container.RWPrx.checkedCast(__base)
#                     __key = identityToString(self.prx.ice_getIdentity())
#                     __cprx.link(__key, self.prx)
#                     logging.info("Object added to '%s'" % __cprx)
#                 else:
#                     logging.error("Proxy especified is not DUO.Container")
#             except Ice.Exception, e:
#                 logging.warning("Couldn't contact with container to add myself!\n%s" % e)
#                 logging.warning("Argument --container-prx will be removed and ignored")
#                 del self.opts["--container-prx"]

#         # Si se indican propiedades
#         if "--np" in self.opts:
#             if "P" in self.iface.split(".")[1]:
#                 # FIXME: use P::T instead
#                 logging.warning("Property Service support not implemented!")

#                 #pairs = self.opts["--np"].split(":")
#                 #props = {}
#                 #for p in pairs:
#                 #    key, value = p.split("=")
#                 #    # FIXME: only strings??
#                 #    props[key] = ASD.strValue(value)
#                 #
#                 #self.servant.setp(props)

#             else:
#                 logging.warning("Not P iface selected. There is no PropertyServer."\
#                                     " 'np' option ignored.")

#         if "--adv-each" in self.opts:
#             if self.__no_announce:
#                 logging.info("ADV disabled! argument '--adv-each' will be ignored")
#             else:
#                 self._timming = int(self.opts["--adv-each"])

#         else:
#             self._timming = 15000

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

    def register_servant(self):
        if not self.args.identity:
            self.proxy = self.adapter.addWithUUID(self.servant)
        else:
            oid = self.communicator().stringToIdentity(self.args.identity)
            self.proxy = self.adapter.add(self.servant, oid)

        logging.info("Proxy used: '{0}'".format(self.proxy))

    def wait(self):
        self.shutdownOnInterrupt()

        ic = self.communicator()
        ic.waitForShutdown()

#         self.servant.prx = self.prx
#         self.setup_announce_topic()

#         if self.prx.ice_isA('::DUO::Active::R'):
#             logging.info("It's an Active object")
#             self.setup_active_topic()


#         if self.prx.ice_isA('::ASD::Search'):
#             logging.info("It is a Search object")
#             try:
#                 asds_channel = self.topicMgr.retrieve("ASDS")
#             except IceStorm.NoSuchTopic:
#                 logging.info("There is no ASDS channel, creating it...")
#                 asds_channel = self.topicMgr.create("ASDS")

#             asds_channel.subscribe({}, self.prx)

#         if self.announce_topic:
#             gobject.timeout_add(self._timming, self.send_adv)
#             self.send_adv()

#         self.gui = self.get_gui()

#         if self.opts.get("render"):
#             signal.signal(signal.SIGINT, gtk.main_quit)
#             gtk.main()

#             self.delete()

    def build_parser(self):
        self.arg_parser = argparse.ArgumentParser(description='Dummy')
        self.arg_parser.add_argument(
            '--id', dest='identity', help='identity of servant')
        self.arg_parser.add_argument(
            '--port', type=int, help='port of object adapter')
        self.arg_parser.add_argument(
            '--host', help='ip where to listen')

    def add_options(self):
        """ To implement on subclass """
        pass


#     def setup_announce_topic(self):
#         self.announce_topic = None

#         properties = self.communicator().getProperties()
#         endpoint = properties.getProperty("IceStorm.TopicManager.Proxy")

#         if not endpoint:
#             logging.warning("Invalid IceStorm.TopicManager.Proxy property")
#             logging.warning("No event service available")
#             return

#         obj = self.communicator().stringToProxy(endpoint)
#         try:
#             self.topicMgr = IceStorm.TopicManagerPrx.checkedCast(obj)
#         except (Ice.ConnectTimeoutException, Ice.ConnectionRefusedException):
#             logging.error("TopicManager unreachable. No event support!")
#             return

#         if self.__no_announce:
#             logging.info("Announce support disabled manually.")
#             return

#         logging.info("ASDA access")
#         try:
#             topic = self.topicMgr.retrieve("ASDA")
#         except IceStorm.NoSuchTopic:
#             topic = self.topicMgr.create("ASDA")
#             logging.warning("There is no ASDA topic. Creating it...")

#         topicPub = topic.getPublisher()
#         self.announce_topic = ASD.ListenerPrx.uncheckedCast(topicPub)


#     def setup_active_topic(self):
#         topic_name = identityToString(self.prx.ice_getIdentity())
#         try:
#             own_topic = self.topicMgr.create(topic_name)
#         except IceStorm.TopicExists:
#             own_topic = self.topicMgr.retrieve(topic_name)
#             logging.warning("Active topic already exists")

#         self.servant.setCbTopic(own_topic.getPublisher(), own_topic)


#     def send_adv(self):
#         self.announce_topic.adv(self.prx, None)
#         logging.info("adv() sent")
#         return True


#     def send_bye(self):
#         self.announce_topic.bye(self.prx.ice_getIdentity())
#         logging.info("bye() sent")

