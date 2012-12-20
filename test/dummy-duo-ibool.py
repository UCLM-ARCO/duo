#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

from signal import SIGINT

from hamcrest import is_not, contains_string

from prego import TestCase, Task, listen_port, localhost


class BoolTests(TestCase):
    def test_set(self):
        port = 1234
        proxy = 'test -t:tcp -p {port}'.format(**locals())

        dummy = Task('dummy', detach=True)
        dummy.assert_that(localhost, is_not(listen_port(port)))

        dummy_options = '--host localhost --port {0} --id test --no-gui W'.format(port)
        dummy_cmd = dummy.exec_cmd(
            './duo-dummy-bool ' + dummy_options, cwd='$basedir/dummies')
        dummy.wait_that(dummy_cmd.stderr.content,
                        contains_string('-> set(True'))

        client = Task('client')
        client.wait_that(localhost, listen_port(port), delta=.05)
        client.exec_cmd("./duo-client-bool '{0}' --set True".format(proxy),
                        cwd='$basedir/clients')

    def test_active(self):
        istaf_port = 11000

        istaf = Task(desc='ISTAF', detach=True)
        istaf.assert_that(localhost, is_not(listen_port(istaf_port)))
        istaf.exec_cmd('duo-istaf',
                       timeout=None,
                       signal=SIGINT, expected=-SIGINT)

        active_port = 1234
        active_proxy = "test -t:tcp -p {0}".format(active_port)

#        active_proxy = "test -t:tcp -p {active_port}"

        active = Task(desc='active actor', detach=True)
        active.assert_that(localhost, is_not(listen_port(active_port)))
        active.wait_that(localhost, listen_port(istaf_port))

        active_options = '--host localhost --port {0} --id test --no-gui RWA'.format(active_port)
        active_cmd = active.exec_cmd(
            './duo-dummy-bool ' + active_options,
            timeout=None,
            cwd='$basedir/dummies',
            signal=SIGINT)

#       active.exec_cmd('./duo-dummy-bool --host localhost --port {active_port} --id test --no-gui RWA'

        active.assert_that(active_cmd.stderr.content,
                           contains_string('-> set(True'))

        observer_port = 1235
        observer = Task(desc='observer', detach=True)
        observer.assert_that(localhost, is_not(listen_port(observer_port)))
        observer.wait_that(localhost, listen_port(active_port))

        observer_options = "--active-suscribe '{}' --host localhost --port {} --id test --no-gui W". format(active_proxy, observer_port)
        observer_cmd = observer.exec_cmd("./duo-dummy-bool " + observer_options,
                                         timeout=None,
                                         cwd='$basedir/dummies',
                                         signal=SIGINT)

        observer.assert_that(observer_cmd.stderr.content,
                             contains_string('-> set(True'))

        client = Task(desc='client')
        client.wait_that(localhost, listen_port(active_port))
        client.wait_that(localhost, listen_port(observer_port))
        client.exec_cmd("./duo-client-bool '{0}' --set True".format(active_proxy),
                        cwd='$basedir/clients')
