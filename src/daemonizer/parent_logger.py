"""
Configure logging helper function with correct UTC name.
"""

import logging
import time


def setup_logging(debug, filename, modname=None):
    """
    Can be imported by ``<my_package>`` to create a log file for logging
    ``<my_package>`` class output.  In this example we use a ``debug``
    flag set in ``<my_package>`` to change the Log Level and ``filename``
    to set log path.  We also use UTC time and force the name in ``datefmt``.
    """
    if debug:
        log_level = logging.getLevelName('DEBUG')
    else:
        log_level = logging.getLevelName('INFO')

    if not modname:
        my_fmt = '%(asctime)s %(levelname)s %(name)s.%(funcName)s(%(lineno)d) %(message)s'
    else:
        my_fmt = (
            '%(asctime)s %(levelname)s %(mod_name)s.%(funcName)s(%(lineno)d) %(message)s'
        )

        default_factory = logging.getLogRecordFactory()

        def record_factory(*args, **kwargs):
            record = default_factory(*args, **kwargs)
            record.mod_name = modname
            return record

        logging.setLogRecordFactory(record_factory)

    logging.basicConfig(
        level=log_level,
        format=my_fmt,
        datefmt='%Y-%m-%d %H:%M:%S UTC',
        filename=filename,
    )

    # BUG: This does not print the TZ name because logging module uses
    #      time instead of tz-aware datetime objects (so we force the
    #      correct name in datefmt above).
    logging.Formatter.converter = time.gmtime

    # To also log parent info, try something like this
    # global logger
    # logger = logging.getLogger("my_package")
