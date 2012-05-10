#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-

# import getopt
# import sys
# import Ice

# Ice.loadSlice("-I/usr/share/Ice/slice -I.. --all ../DUO.ice")
# import DUO


# def catchIceExc(fn):
#     def __deco(self, *args, **kwargs):
#         try:
#             return fn(self, *args, **kwargs)
#         except Ice.Exception, e:
#             print "There were an error:", e
#     return __deco


# class App(Ice.Application):
#     def __init__(self):
#         self.options = {}

#     def usage(self):
#         print "USAGE:", sys.argv[0], "<proxy> <cmd> <opts>\n"\
#             "Where cmd may be:\n"\
#             "   --get               Return value of object.\n"\
#             "   --set {True,False}  Set value of object to given.\n"\
#             "\n"\
#             "And opts may be:\n"\
#             "   --facet name        Use given facet of proxy.\n"

#     def parseOptions(self, args):
#         args = args[1:]

#         try:
#             if args[0].startswith("--"):
#                 raise IndexError

#             self.options['proxy'] = args[0]
#             args = args[1:]

#         except IndexError:
#             print "Invalid arguments."
#             self.usage()
#             return False

#         try:
#             opts, args = getopt.getopt(args, "", ['set=', 'get', 'facet='])

#         except getopt.GetoptError, opt:
#             print "There is problem with options, '%s'" % opt
#             self.usage()
#             return False

#         self.options.update(opts)

#         if "--set" in self.options:
#             self.options["cmd"] = "set"
#         elif "--get" in self.options:
#             self.options["cmd"] = "get"
#         else:
#             print "Please, provide a command to execute!"
#             self.usage()
#             return False

#         return True

#     @catchIceExc
#     def run(self, args):
#         if not self.parseOptions(args):
#             return -1

#         self.base = self.communicator().stringToProxy(self.options["proxy"])

#         if self.options.has_key("--facet"):
#             self.base = self.base.ice_facet(self.options["--facet"])

#         return {"set":self.__do_set,
#                 "get":self.__do_get,
#                 }[self.options["cmd"]]()

#     @catchIceExc
#     def __do_set(self):
#         prx = DUO.IBool.WPrx.checkedCast(self.base)
#         if not prx:
#             print "Given proxy is not an IBool.W"
#             return -1

#         value = self.options["--set"].lower() == "true"
#         prx.set(value, Ice.Identity())
#         return 0

#     @catchIceExc
#     def __do_get(self):
#         prx = DUO.IBool.RPrx.checkedCast(self.base)
#         if not prx:
#             print "Given proxy is not an IBool.R"
#             return -1

#         print prx.get()
#         return 0



# if __name__ == "__main__":
#     App().main(sys.argv, "config")
