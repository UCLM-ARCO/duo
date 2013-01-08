#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

from signal import SIGINT

from hamcrest import is_not, contains_string

from prego import TestCase, Task, context
from prego.net import listen_port, localhost


class BoolTests(TestCase):
    def test_set(self):
        context.port = 1234
        context.proxy = 'test -t:tcp -p $port'

        dummy = Task('dummy', detach=True)
        dummy.assert_that(localhost, is_not(listen_port(context.port)))

        dummy_options = '--host localhost --port $port --id test --no-gui W'
        dummy.command('./duo-dummy-bool ' + dummy_options,
                      cwd='$basedir/dummies')
        dummy.wait_that(dummy.lastcmd.stderr.content,
                        contains_string('-> set(True'))

        client = Task('client')
        client.wait_that(localhost, listen_port(context.port), delta=.05)
        client.command("./duo-client-bool '$proxy' --set True",
                       cwd='$basedir/clients')

    def test_active(self):
        context.istaf_port = 11000
        context.active_port = 1234
        context.active_proxy = "test -t:tcp -p $active_port"
        context.observer_port = 1235

        istaf = Task(desc='ISTAF', detach=True)
        istaf.assert_that(localhost, is_not(listen_port(context.istaf_port)))
        istaf.command('duo-istaf',
                      timeout=None, signal=SIGINT, expected=-SIGINT)

        active = Task(desc='active actor', detach=True)
        active.assert_that(localhost, is_not(listen_port(context.active_port)))
        active.wait_that(localhost, listen_port(context.istaf_port))

        active_options = '--host localhost --port $active_port --id test --no-gui RWA'
        active_cmd = active.command('./duo-dummy-bool ' + active_options,
                                    cwd='$basedir/dummies',
                                    timeout=None, signal=SIGINT)

        active.assert_that(active_cmd.stderr.content,
                           contains_string('-> set(True'))

        observer = Task(desc='observer', detach=True)
        observer.assert_that(localhost, is_not(listen_port(context.observer_port)))
        observer.wait_that(localhost, listen_port(context.active_port))

        observer_options = "--active-suscribe '$active_proxy' --host localhost --port $observer_port --id test --no-gui W"
        observer.command("./duo-dummy-bool " + observer_options,
                         cwd='$basedir/dummies',
                         timeout=None, signal=SIGINT)

        observer.assert_that(observer.lastcmd.stderr.content,
                             contains_string('-> set(True'))

        client = Task(desc='client')
        client.wait_that(localhost, listen_port(context.active_port))
        client.wait_that(localhost, listen_port(context.observer_port))
        client.command("./duo-client-bool '$active_proxy' --set True",
                       cwd='$basedir/clients')
