# -*- coding: utf-8 -*-
import os
import sys
import time
import unittest

from daemon import Daemon

import settings as s
from daemon.parent_logger import setup_logging


if s.DEBUG:
    debug = True


class TDaemon(Daemon):
    def __init__(self, *args, **kwargs):
        super(TDaemon, self).__init__(*args, **kwargs)
        testoutput = open('testing_daemon', 'w')
        testoutput.write('inited')
        testoutput.close()

    def run(self):
        time.sleep(0.3)
        testoutput = open('testing_daemon', 'w')
        testoutput.write('finished')
        testoutput.close()


def control_daemon(action):
    os.system(" ".join((sys.executable, __file__, action)))


class TestDaemon(unittest.TestCase):
    testoutput = None

    def setUp(self):
        control_daemon('start')
        time.sleep(0.1)
        self.testoutput = open('testing_daemon')

    def test_daemon_can_start(self):
        assert os.path.exists(s.PIDFILE)
        assert self.testoutput.read() == 'inited'

    def test_daemon_can_stop(self):
        control_daemon('stop')
        time.sleep(0.1)
        assert os.path.exists(s.PIDFILE) is False
        assert self.testoutput.read() == 'inited'

    def test_daemon_can_finish(self):
        time.sleep(0.4)
        assert os.path.exists(s.PIDFILE) is False
        assert self.testoutput.read() == 'finished'

    def test_daemon_can_restart(self):
        assert os.path.exists(s.PIDFILE)
        pidfile = open(s.PIDFILE)
        pid1 = pidfile.read()
        pidfile.close()
        control_daemon('restart')
        time.sleep(0.1)
        assert os.path.exists(s.PIDFILE)
        pidfile = open(s.PIDFILE)
        pid2 = pidfile.read()
        pidfile.close()
        assert pid1 != pid2

    def tearDown(self):
        self.testoutput.close()
        if os.path.exists(s.PIDFILE):
            control_daemon('stop')
        time.sleep(0.05)
        os.system('rm testing_daemon*')


if __name__ == '__main__':
    setup_logging(debug, s.LOGFILE)
    if len(sys.argv) == 1:
        unittest.main()
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg in ('start', 'stop', 'restart'):
            d = TDaemon(s.PIDFILE, verbose=1)
            getattr(d, arg)()
