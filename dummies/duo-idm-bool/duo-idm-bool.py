#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-

from flask import Flask, render_template


# class IBoolWI(Dummy.IBoolW):
#     def __init__(self, args):
#         self.state = args.state
#         self.address = args.address

#     def set(self, state, source, current):
#         pass

#     def setObserver(self, observer, current):
#         pass


class WebServer:
    app = Flask(__name__)

    def run(self):
        self.app.run(debug=True, threaded=True)

    @app.route("/")
    def index():
        context = {'state': 'true'}
        return render_template("index.html", **context)


if __name__ == "__main__":
    WebServer().run()
