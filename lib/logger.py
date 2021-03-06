u'''Simple wrapper around python's logging package'''

from __future__ import absolute_import
import os
import logging
from logging import handlers
from twisted.python import log as twisted_log

from . import settings

u'''
class Logger(object):
    def debug(self, msg):
        twisted_log.msg(msg)

    def info(self, msg):
        twisted_log.msg(msg)

    def warning(self, msg):
        twisted_log.msg(msg)

    def error(self, msg):
        twisted_log.msg(msg)

    def critical(self, msg):
        twisted_log.msg(msg)
'''


def get_logger(name):
    logger = logging.getLogger(name)
    logger.addHandler(stream_handler)
    logger.setLevel(getattr(logging, settings.LOGLEVEL))

    if settings.LOGFILE is not None:
        logger.addHandler(file_handler)

    logger.debug(u"Logging initialized")
    return logger
    # return Logger()

if settings.DEBUG:
    fmt = logging.Formatter(
        u"%(asctime)s %(levelname)s %(name)s %(module)s.%(funcName)s # %(message)s")
else:
    fmt = logging.Formatter(u"%(asctime)s %(levelname)s %(name)s # %(message)s")

if settings.LOGFILE is not None:
    # Create the log folder if it does not exist
    try:
        os.makedirs(os.path.join(os.getcwdu(), settings.LOGDIR))
    except OSError:
        pass

    # Setup log rotation if specified in the config
    if settings.LOG_ROTATION:
        file_handler = logging.handlers.RotatingFileHandler(
            os.path.join(
                settings.LOGDIR,
                settings.LOGFILE),
            u'a',
            settings.LOG_SIZE,
            settings.LOG_RETENTION)
    else:
        file_handler = logging.handlers.WatchedFileHandler(
            os.path.join(settings.LOGDIR, settings.LOGFILE))
    file_handler.setFormatter(fmt)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(fmt)
