# -*- coding: utf-8 -*-
'''
***
Modified generic daemon class
***

Author:         http://www.jejik.com/articles/2007/02/
                        a_simple_unix_linux_daemon_in_python/www.boxedice.com

License:        http://creativecommons.org/licenses/by-sa/3.0/

Changes:        23rd Jan 2009 (David Mytton <david@boxedice.com>)
                - Replaced hard coded '/dev/null in __init__ with os.devnull
                - Added OS check to conditionally remove code that doesn't
                  work on OS X
                - Added output to console on completion
                - Tidied up formatting
                11th Mar 2009 (David Mytton <david@boxedice.com>)
                - Fixed problem with daemon exiting on Python 2.4
                  (before SystemExit was part of the Exception base)
                13th Aug 2010 (David Mytton <david@boxedice.com>)
                - Fixed unhandled exception if PID file is empty
                12th Mar 2020 (Stephen Arnold <nerdboy@gentoo.org>)
                - add status arg, utc timestamp/logging helpers, tag 0.2.3
'''

# Core modules
from __future__ import print_function

import atexit
import datetime
import errno
import logging
import os
import signal
import sys
import time

try:
    from datetime import timezone
    utc = timezone.utc  # pragma: PY3
except ImportError:  # pragma: PY2
    from daemon.timezone import UTC
    utc = UTC()  # type: ignore

from ._version import __version__

logger = logging.getLogger(__name__)
utc_stamp = datetime.datetime.now(utc)


def timestamp():
    """
    Make a UTC timestamp.
    """
    # sys.stdout.write('='*80)
    sys.stdout.write(f'\nTIMESTAMP v{__version__}: ')
    sys.stdout.write('{:%Y-%m-%d %H:%M:%S %Z}\n'.format(utc_stamp))


class Daemon():
    """
    A generic daemon class.

    Usage: subclass the Daemon class and override the run() method
    """
    def __init__(self, pidfile, stdin=os.devnull,
                 stdout=os.devnull, stderr=os.devnull,
                 home_dir='.', umask=0o22, verbose=1,
                 use_gevent=False, use_eventlet=False,
                 use_cleanup=False):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        self.home_dir = home_dir
        self.verbose = verbose
        self.umask = umask
        self.daemon_alive = True
        self.use_gevent = use_gevent
        self.use_eventlet = use_eventlet
        self.use_cleanup = use_cleanup

    def log(self, *args):
        if self.verbose >= 1:
            print(*args)

    def daemonize(self):
        """
        Do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        if self.use_eventlet:
            import eventlet.tpool
            eventlet.tpool.killall()
        try:
            pid = os.fork()
            if pid > 0:
                # Exit first parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write(
                "fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # Decouple from parent environment
        os.chdir(self.home_dir)
        os.setsid()
        os.umask(self.umask)

        # Do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # Exit from second parent
                sys.exit(0)
        except OSError as e:
            sys.stderr.write(
                "fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        if sys.platform != 'darwin':  # This block breaks on OS X
            # Redirect standard file descriptors
            sys.stdout.flush()
            sys.stderr.flush()
            si = open(self.stdin, 'r')
            so = open(self.stdout, 'a+')
            if self.stderr:
                try:
                    se = open(self.stderr, 'a+', 0)
                except ValueError:
                    # Python 3 can't have unbuffered text I/O
                    se = open(self.stderr, 'a+', 1)
            else:
                se = so
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(se.fileno(), sys.stderr.fileno())

        def sigtermhandler(signum, frame):  # pylint: disable=W0613
            if self.use_cleanup:
                self.cleanup()
                time.sleep(0.1)
            self.daemon_alive = False
            sys.exit()

        if self.use_gevent:
            import gevent
            gevent.reinit()
            gevent.signal_handler(signal.SIGTERM, sigtermhandler, signal.SIGTERM, None)
            gevent.signal_handler(signal.SIGINT, sigtermhandler, signal.SIGINT, None)
        else:
            signal.signal(signal.SIGTERM, sigtermhandler)
            signal.signal(signal.SIGINT, sigtermhandler)

        if self.verbose:
            timestamp()
            self.log("Started")
        else:
            logger.info('Started')

        # Write pidfile
        atexit.register(
            self.delpid)  # Make sure pid file is removed if we quit
        pid = str(os.getpid())
        open(self.pidfile, 'w+', encoding='utf-8').write(f"{pid}\n")

    def delpid(self):
        """
        Remove PID file if they are us.
        """
        try:
            # the process may fork itself again
            pid = int(open(self.pidfile, 'r', encoding='utf-8').read().strip())
            if pid == os.getpid():
                os.remove(self.pidfile)
        except OSError as e:
            if e.errno == errno.ENOENT:
                pass
            else:
                raise

    def start(self, *args, **kwargs):
        """
        Start the daemon
        """

        if self.verbose:
            timestamp()
            self.log("Starting...")
        else:
            logger.info('Starting...')

        # Check for a pidfile to see if the daemon already runs
        try:
            pfile = open(self.pidfile, 'r', encoding='utf-8')
            pid = int(pfile.read().strip())
            pfile.close()
        except IOError:
            pid = None
        except SystemExit:
            pid = None

        if pid:
            message = "pidfile %s already exists. Is it already running?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run(*args, **kwargs)

    def status(self):
        """
        Get status from the daemon
        """

        if not self.is_running():
            message = "pidfile %s does not exist. Not running?\n"
            sys.stderr.write(message % self.pidfile)
        else:
            message = "pidfile %s found, daemon PID is %d\n"
            sys.stdout.write(message % (self.pidfile, self.get_pid()))

        if self.verbose >= 1:
            timestamp()
            self.log(f"{__name__} status is: {self.is_running()}")

        return self.is_running()

    def stop(self):
        """
        Stop the daemon
        """

        if self.verbose >= 1:
            timestamp()
            self.log("Stopping...")
        else:
            logger.info('Stopping...')

        # Get the pid from the pidfile
        pid = self.get_pid()

        if not pid:
            message = "pidfile %s does not exist. Not running?\n"
            sys.stderr.write(message % self.pidfile)

            # Just to be sure. A ValueError might occur if the PID file is
            # empty but does actually exist
            if os.path.exists(self.pidfile):
                os.remove(self.pidfile)

            return  # Not an error in a restart

        # Try killing the daemon process
        try:
            i = 0
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
                i = i + 1
                if i % 10 == 0:
                    os.kill(pid, signal.SIGHUP)
        except OSError as err:
            if err.errno == errno.ESRCH:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err))
                sys.exit(1)

        self.log("Stopped")

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def cleanup(self):
        """
        You should override this method if you need cleanup handlers on
        shutdwon (ie, prior to sigterm handling) and set use_cleanup to
        ``True`` when you subclass daemon().
        """
        raise NotImplementedError

    def get_pid(self):
        """
        Get process ID.

        :return pid: daemon process ID
        :rtype int:
        """
        try:
            pfile = open(self.pidfile, 'r', encoding='utf-8')
            pid = int(pfile.read().strip())
            pfile.close()
        except IOError:
            pid = None
        except SystemExit:
            pid = None
        return pid

    def is_running(self):
        """
        Check whether the server is running.

        :return: True if running, else False
        """
        pid = self.get_pid()

        if pid is None:
            logger.debug('Process is stopped')
            return False
        if os.path.exists(f'/proc/{pid}'):
            logger.debug('Process (pid %d) is running...', pid)
            return True
        logger.debug('Process (pid %d) is killed', pid)
        return False

    def run(self):
        """
        You should override this method when you subclass Daemon.
        It will be called after the process has been
        daemonized by start() or restart().
        """
        raise NotImplementedError
