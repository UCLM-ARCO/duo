#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

# """
# Options: --no-gui                 : launch it without GUI.
#          --no-announce            : launch it without event support.
#          --id identity            : identity of servant.
#          --port num_port          : port of object adapter.
#          --host ip                : ip where listen.
#          --init state             : initial state, [true,false].
#          --container-prx prx      : container proxy on wich add itself
#                                     (of type DUO.iContainer).
#          --hide-dummy-iface       : hides dummy interface from ice introspection
#          --add-fake-ifaces iface   : append iface to ids for this object.
#          --fake-ifaces iface1, iface2, ... : use iface1, iface2... as ids for this object
#          --adv-each ms            : announce each ms millisencods.

#          --on-image filename      : image to show when on.
#          --off-image filename     : image to show when off.

#          --np key1=value1:key2... : set new property pairs (key,value)
#                                     (only when iface P used).
# """


import sys
# import getopt

# import gtk
# import gtk.glade

import dummyBase as base


# class BoolGUI(base.GUI):
#     def __init__(self, opts, *args):
#         glade = gtk.glade.XML("toggle.glade", "togglebutton")
#         self.gui = glade.get_widget("togglebutton")
#         glade.signal_autoconnect(self)

#         self.off = glade.get_widget("image_off")
#         self.on = glade.get_widget("image_on")

#         self.on.set_from_file(opts.get('--on-image', 'pixmaps/bulb-true.png'))
#         self.off.set_from_file(opts.get('--off-image', 'pixmaps/bulb-false.png'))

#         # Por defect, off
#         self.on.hide()

#         base.GUI.__init__(self, *args)


#     def update(self):
#         self.gui.set_active(self.model.state)
#         base.GUI.update(self)


#     def on_togglebutton_toggled(self, widget):
#         self.model.set_state(widget.get_active())
#         if widget.get_active():
#             self.off.hide()
#             self.on.show()
#         else:
#             self.on.hide()
#             self.off.show()


class DummyBool(base.Dummy):

    def add_options(self):
        self.arg_parser.add_argument(
            'interface', choices=('R', 'W', 'RW'), type=str,
            help='interface to implement')
        self.arg_parser.add_argument(
            '--init', dest='state', type=bool, help="initial state",
            default=False)

    def create_servant(self):
        iface = "IBool.{0}".format(self.args.interface)
        dummyClass = base.MetaDummy(iface)
        self.servant = dummyClass(self.args.state)

#     def get_gui(self):
#         if "--no-gui" in self.opts:
#             base.logging.info("GUI disabled manually.")
#             return None

#         return BoolGUI(self.opts, self.servant, self.iface, str(self.prx))



# def createNew(opts):
#     return DummyBool("IBool." + opts["iface"], opts)


# def usage():
#     base.usage('Actor.IBool')
#     print __doc__
#     return 1



if __name__ == "__main__":
    dummy = DummyBool()
    sys.exit(dummy.main(sys.argv))

#     try:
#         opts, args = getopt.getopt(sys.argv[1:], "",
#                                    ['on-image=', 'off-image=',
#                                     'no-gui', 'no-announce', 'id=', 'port=', 'host=', 'init=',
#                                     'container-prx=', 'np=', 'adv-each=', 'hide-dummy-iface',
#                                     'add-fake-ifaces=', 'fake-ifaces=', 'Ice.Config='])
#     except getopt.GetoptError, opt:
#         print opt, "\n"
#         sys.exit(usage())

# #    options = {}
# #    for i in opts:
# #        options[i[0]] = i[1]
#     options = dict(opts)

#     if len(args) < 1:
#         sys.exit(usage())

#     options["iface"] = args[0]
#     options["render"] = True
# #    createNew(options).main(sys.argv, "config")
#     createNew(options).main(sys.argv)
