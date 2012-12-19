# -*- mode: python; coding: utf-8 -*-

import logging

from gi.repository import Gtk, GObject
GObject.threads_init()


class DummyColorBand(Gtk.DrawingArea):
    def __init__(self):
        Gtk.DrawingArea.__init__(self)
        self.w = 20
        self.h = 20

    def do_draw(self, ctx):
        width = self.get_allocation().width
        n = width / self.w

        for i in range(0, n + 2):
            ctx.move_to(i * self.w, 0)
            ctx.line_to(i * self.w + self.w, 0)
            ctx.line_to(i * self.w, self.h)
            ctx.line_to(i * self.w - self.w, self.h)
            ctx.close_path()
            if i % 2:
                ctx.set_source_rgb(1, 0.83, 0.16)
            else:
                ctx.set_source_rgb(0, 0, 0)
            ctx.fill_preserve()
            ctx.set_source_rgb(0, 0, 0)
            ctx.stroke()


class TextAreaStream(file):
    def __init__(self, textview):
        self.textview = textview
        self.buffer = textview.get_buffer()

    def write(self, msg):
        GObject.idle_add(self.buffer.insert_at_cursor, msg)
        GObject.idle_add(self.textview.scroll_mark_onscreen, self.buffer.get_insert())

    def flush(self):
        pass


class GladeWrapper(object):
    def __init__(self, filename, widget='window'):
        self._builder = Gtk.Builder()
        self._builder.add_from_file(filename)
        self._builder.connect_signals(self)

        self._widget = self.wg_window

    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except KeyError, e:
            if name.startswith("wg_"):
                ret = self._builder.get_object(name[3:])
                if ret:
                    self.__dict__[name] = ret
                    return ret
            raise AttributeError("{0}: {1}".format(str(self.__class__), e))


class GUI(GladeWrapper):
    def __init__(self, model):
        GladeWrapper.__init__(self, "dummy.glade")
        self._model = model
        self._model.attach(self)

        self._setup_gui()
        self._add_dummy_bands()

    def _setup_gui(self):
        widget = self.create_content()
        self.wg_content.pack_start(widget, False, False, 0)
        self.wg_proxy.set_text(
            self._model.get_proxy_as_string())

        if self._model.is_duo_active():
            self.wg_observer_label.show()
            self.wg_observer_proxy.set_text(
                self._model.get_observer_as_string())
            self.wg_observer_proxy.show()

        self._setup_logging()

    def _setup_logging(self):
        handler = logging.StreamHandler(TextAreaStream(self.wg_log))
        logging.getLogger().addHandler(handler)

    def create_content(self):
        """To implement on children"""
        raise NotImplementedError

    def _add_dummy_bands(self):
        top_band = DummyColorBand()
        top_band.set_size_request(-1, top_band.h)
        self.wg_box_main.pack_start(top_band, False, False, 0)
        self.wg_box_main.reorder_child(top_band, 0)

        bottom_band = DummyColorBand()
        bottom_band.set_size_request(-1, bottom_band.h)
        self.wg_box_main.pack_end(bottom_band, False, False, 0)

    def show(self):
        self._widget.show_all()

    def on_quit(self, *args):
        self._model.loop.quit()

    def __str__(self):
        return self.__class__.__name__
