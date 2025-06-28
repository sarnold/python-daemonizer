# -*- coding: utf-8 -*-
import os
import sys
import time
import unittest
from test import settings as s

from daemonizer import Daemon
from daemonizer.parent_logger import setup_logging

if s.DEBUG:
    debug = True


class TDaemon(Daemon):
    def __init__(self, *args, **kwargs):
        super(TDaemon, self).__init__(*args, **kwargs)
        testoutput = open('testing_daemon', 'w')
        testoutput.write('inited')
        testoutput.close()

    def cleanup(self):
        testoutput = open('testing_daemon', 'w')
        testoutput.write('cleanup')
        testoutput.close()

    def run(self):
        time.sleep(0.5)
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
        time.sleep(0.45)
        assert self.testoutput.read() == 'cleanup'
        assert os.path.exists(s.PIDFILE) is False

    def test_daemon_can_finish(self):
        time.sleep(0.6)
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

    # unittest+pytest makes these difficult to get output for assertions
    # although correct output can be seen with --capture=no
    def test_daemon_status_false(self):
        control_daemon('stop')
        time.sleep(0.1)
        control_daemon('status')

    def test_daemon_status_true(self):
        assert os.path.exists(s.PIDFILE)
        control_daemon('status')

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
        if arg in ('start', 'stop', 'restart', 'status'):
            d = TDaemon(s.PIDFILE, verbose=1, use_cleanup=True)
            getattr(d, arg)()
