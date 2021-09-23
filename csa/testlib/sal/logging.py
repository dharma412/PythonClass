from __future__ import absolute_import

# !/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/sal/logging.py#1 $
#
# Logger objects used by iaf2 modules.
#
# Two types of logger objects available: Text Loggers or Gui Loggers
#
# log levels:   CRITICAL FATAL ERROR WARNING WARN INFO DEBUG NOTSET
#               RAW PASSED FAILED ERRORED ABORTED NOTIMPLEMENTED

#: Reference Symbols: iaflogger

import logging
import sys
import os
import re
import shutil

from sal.deprecated import guilog

# logger_fmt          = '%(asctime)s:%(levelname)s: %(message)s'
# logger_fmt          = '%(asctime)s.%(msecs)d:%(levelname)s: %(message)s'
logger_fmt = '%(levelname)s: %(message)s'
time_fmt = '%y%m%d%H%M%S'

orig_stdout = sys.stdout
orig_stderr = sys.stderr

"""
    Customized logging module.

    When called from runtest, you have:
        Globally available loggers:
          global_logger
          stdout_logger
          result_logger
          empty_result_logger
        DUT loggers:
          cli_logger.<hostname>
          shell_logger.<hostname>
          gui_logger.<hostname>
          euqgui_logger.<hostname>
          corpus loggers.<hostname>
          corpush_logger.<hostname>
          corpusgui_logger.<hostname>
        Misc loggers:
          nullsmtpd_logger
          smtpspam_logger
"""

# Global dictionary of instantiated logger objects.
loggers = {
    # 'logger name': IafLogger object,
}

# initialize_factories() called later in this module initializes these globals
tl_factory = None  # Text Logger Factory
gl_factory = None  # Gui Logger Factory

# causes setup_loggers() to return immediately if this flag is set to True
is_loggers_setup_run = False

##################################
# START: Modify stock logging module
##################################
RAW = logging.DEBUG + 1
NOTIMPLEMENTED = logging.ERROR - 1
PASSED = logging.ERROR + 1
ABORTED = logging.ERROR + 2
FAILED = logging.ERROR + 3
ERRORED = logging.ERROR + 4


def emit(self, record):
    """Emit a record.
    Change from stock StreamHandler.emit():
        * handle RAW level:
            * Do not format raw messages. Write raw bytes.
            * Do not append newline to raw message.
    """

    def _prepend_newline(self, level, msg):
        if not hasattr(self, '_last_char'):
            self._last_char = '\n'

        if level != 'RAW':
            if self._last_char != '\n':
                msg = '\n' + msg  # need a newline
        # else don't prepend \n for RAW records

        if len(msg) > 0:
            self._last_char = msg[-1]
        # else don't update self._last_char

        return msg

    if record.levelname == 'RAW':
        msg = record.message = record.getMessage()
    else:
        msg = self.format(record) + '\n'

    msg = _prepend_newline(self, record.levelname, msg)
    try:
        self.stream.write(msg)
    except (UnicodeError, ValueError):
        try:
            self.stream.write(msg.encode("UTF-8"))
        except ValueError as err:
            print err
    except IOError:
        print "WARNING!! Logger couldn't write to file..."
    try:
        self.flush()
    except ValueError as err:
        print err


class IafLogger(logging.Logger):
    """Extend Logger and add convenience methods to wrap new Logger levels.
    IafLogger behaves like a file object (since write, flush, close exist)."""

    def passed(self, msg=''):
        self.log(PASSED, msg)

    def failed(self, msg='', exc_info=False):
        self.log(FAILED, msg, exc_info=exc_info)

    def errored(self, msg='', exc_info=False):
        self.log(ERRORED, msg, exc_info=exc_info)

    error = errored  # alias: overwrite stock error() method with our own

    def aborted(self, msg='', exc_info=False):
        self.log(ABORTED, msg, exc_info=exc_info)

    def notimplemented(self, msg=''):
        self.log(NOTIMPLEMENTED, msg)

    def close(self):
        for h in self.handlers:
            if getattr(h, 'close', None):
                h.close()

    def raw(self, msg=''):
        self.log(RAW, msg)

    write = raw  # write() is an alias

    def flush(self):
        for h in self.handlers:
            if getattr(h, 'flush', None):
                h.flush()

    def isatty(self):
        return True


logging.StreamHandler.emit = emit  # Set Iaf specific emit()

logging.addLevelName(RAW, 'RAW')
logging.addLevelName(NOTIMPLEMENTED, 'RESULT:NOTIMPLEMENTED')
logging.addLevelName(PASSED, 'RESULT:PASSED')
logging.addLevelName(ABORTED, 'RESULT:ABORTED')
logging.addLevelName(FAILED, 'RESULT:FAILED')
logging.addLevelName(ERRORED, 'RESULT:ERRORED')
logging.setLoggerClass(IafLogger)  # Set default logger to IafLogger


##################################
# END: Modify stock logging module
##################################


##################################
# START: Logger Factory Classes
##################################
class IafLoggerFactoryBase:
    log_dir_base = None  # this will be set by the child class once
    log_base_set = False
    relative_root_dir = ''  # this defaults to empty

    def set_log_dir_base(self, log_dir_base):
        if not self.log_base_set:
            self.log_dir_base = log_dir_base
            self.log_base_set = True

    def set_root_dir(self, root_dir):
        self.relative_root_dir = root_dir

    def get_curr_root_dir(self):
        return os.path.normpath('/'.join((self.log_dir_base,
                                          self.relative_root_dir)))


class IafTextLoggerFactory(IafLoggerFactoryBase):
    def __init__(self, biglog_file_obj=None):
        global logger_fmt, time_fmt
        self._biglog_file_obj = biglog_file_obj
        self._fmt = logger_fmt
        self._time_fmt = time_fmt

    def set_biglog_file_obj(self, biglog_file_obj):
        self._biglog_file_obj = biglog_file_obj

    def create(self, log_dir_base, log_name=None, basename='', host='',
               backup_qty=10, stdout_level=None):
        self.set_log_dir_base(log_dir_base)
        filename = os.path.join(self.log_dir_base,
                                self.relative_root_dir,
                                host,
                                basename)

        #
        # NOTE: log_name contains host
        #
        if host:
            log_name += '.' + host
        logger = self.create_core(log_name, filename, stdout_level, backup_qty)
        return logger

    def create_core(self, log_name, filename, stdout_level=None, backup_qty=10):
        global loggers
        global orig_stdout, orig_stderr
        assert not loggers.has_key(log_name), \
            'logger(%s) already exists' % log_name

        # create logger
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)  # log everything by default

        # 1. write to log file
        file_obj = create_file_obj(filename, backup_qty=backup_qty)
        hdlr = logging.StreamHandler(file_obj)
        hdlr.setFormatter(logging.Formatter(self._fmt, self._time_fmt))
        logger.addHandler(hdlr)

        # 2. write to biglog
        if self._biglog_file_obj:
            hdlr = logging.StreamHandler(self._biglog_file_obj)
            hdlr.setFormatter(logging.Formatter(logger_fmt, time_fmt))
            logger.addHandler(hdlr)

        # 3. write to stdout
        hdlr = logging.StreamHandler(orig_stdout)
        hdlr.setFormatter(logging.Formatter(logger_fmt, time_fmt))
        logger.addHandler(hdlr)
        hdlr.setLevel(stdout_level or logging.INFO)

        # update global 'loggers' dictionary
        loggers[log_name] = logger

        return logger


class IafGuiLoggerFactory(IafLoggerFactoryBase):
    def get_log_dirname(self, log_basedir, host=''):
        dirname = os.path.normpath(
            '/'.join((self.log_dir_base, self.relative_root_dir, host,
                      log_basedir)))
        return dirname

    def create(self, log_dir_base, log_name, log_basedir='', host=''):
        self.set_log_dir_base(log_dir_base)
        dirname = self.get_log_dirname(log_basedir, host)

        #
        # NOTE: log_name contains host
        #

        if host:
            log_name += '.' + host
        logger = self.create_core(log_name, dirname)
        return logger

    def create_core(self, log_name, dirname):
        global loggers
        assert not loggers.has_key(log_name), \
            'logger(%s) already exists' % log_name
        logger = guilog.GlobalGuiLogInterface(dirname)
        # update global 'loggers' dictionary
        loggers[log_name] = logger
        return logger


##################################
# END: Logger Creater Classes
##################################

##################################
# START: Utility Functions
##################################

def create_dir(dir_name):
    if not os.path.exists(dir_name) and dir_name:
        os.makedirs(dir_name)
    try:
        os.chmod(dir_name, 0777)
    except Exception, e:
        pass


def create_file_obj(log_filename, mode='w', do_rollover=True, backup_qty=10):
    # create log directory
    dir_name = os.path.dirname(log_filename)

    create_dir(dir_name)
    # create log file (and rotate)
    if do_rollover:
        rollover(log_filename, backup_qty)
    log_file_obj = open(log_filename, mode, 0)  # no buffering
    os.chmod(log_filename, 0666)
    return log_file_obj


def rollover(log_filename, backup_qty=10):
    """modified code from logging.handlers.RotatingFileHandler"""
    if backup_qty > 0 and os.path.exists(log_filename):
        for i in range(backup_qty - 1, 0, -1):
            sfn = "%s.%d" % (log_filename, i)
            dfn = "%s.%d" % (log_filename, i + 1)
            dfn = "%s.%d" % (log_filename, i + 1)
            if os.path.exists(sfn):
                if os.path.exists(dfn):
                    os.remove(dfn)
                os.rename(sfn, dfn)
        dfn = log_filename + ".1"
        if os.path.exists(dfn):
            os.remove(dfn)
        os.rename(log_filename, dfn)


def rollover_root_dir(root_dir, backup_qty=10):
    """modified code from logging.handlers.RotatingFileHandler"""
    if backup_qty > 0 and os.path.exists(root_dir):
        for i in range(backup_qty - 1, 0, -1):
            sfn = "%s.%d" % (root_dir, i)
            dfn = "%s.%d" % (root_dir, i + 1)
            if os.path.exists(sfn):
                if os.path.exists(dfn):
                    shutil.rmtree(dfn, ignore_errors=False)
                os.rename(sfn, dfn)
        dfn = root_dir + ".1"
        if os.path.exists(dfn):
            shutil.rmtree(root_dir, ignore_errors=True)
        os.rename(root_dir, dfn)


##################################
# END: Utility Functions
##################################

##################################
# START: LOGGER CREATOR/GETTERS
##################################

def initialize_factories():
    global tl_factory, gl_factory
    tl_factory = IafTextLoggerFactory()  # Text Logger Factory
    gl_factory = IafGuiLoggerFactory()  # Gui Logger Factory


def reset_loggers(log_dir_base, root_dir, stdout_level=None):
    """Rerun setup_loggers() and point all known loggers
    to the new root_dir."""
    global is_loggers_setup_run
    for name, logger in loggers.items():
        if hasattr(logger, 'handlers'):
            for handler in logger.handlers:
                handler.flush()
                handler.close()
            del logging.Logger.manager.loggerDict[name]
        else:
            logger.close()
        del loggers[name]
    is_loggers_setup_run = False
    setup_loggers(log_dir_base, root_dir, stdout_level)


def setup_loggers(log_dir_base, root_dir=None, stdout_level=None,
                  log_backup_qty=10):
    """- create 1) biglog logger and 2) stdout logger.
    - all subsequent loggers created will to biglog in addition
      to the specified log file.
    - All loggers write to the directory specified by root_dir.
    - A logger object can be treated like a regular log file object
      (ie. it has write(), flush(), close() methods).
    - stdout and stderr are both redirected to stdout.log file.
    """
    global is_loggers_setup_run

    # Should be replaced with initialize_factories_if_neccesary decorator
    if not tl_factory:
        initialize_factories()

    if is_loggers_setup_run:
        return
    is_loggers_setup_run = True

    # NOTE: create loggers before stdout, stderr are redefined!

    # all log files are relative to log_dir_base/relative_root_dir
    if root_dir:
        tl_factory.set_root_dir(root_dir)
        gl_factory.set_root_dir(root_dir)
    dir = '/'.join((log_dir_base, root_dir))
    # rollover the root log directory
    rollover_root_dir(dir, log_backup_qty)

    tl_factory.set_biglog_file_obj(None)

    # Write pass, fail, abort, etc results to log
    create_text_logger(log_dir_base, 'result_logger', 'result.log',
                       stdout_level=logging.NOTSET)
    # Write IafTestNotImplemented, IafEmptyTestResult results to log
    create_text_logger(log_dir_base, 'empty_result_logger', 'empty_result.log',
                       stdout_level=logging.NOTSET)

    create_text_logger(log_dir_base, 'global_logger', 'biglog.log',
                       stdout_level=stdout_level)

    # All loggers will now also write to biglog.log
    biglog_file_obj = get_logger('global_logger')
    tl_factory.set_biglog_file_obj(biglog_file_obj)

    create_text_logger(log_dir_base, 'stdout_logger', 'stdout.log',
                       stdout_level=(stdout_level or logging.DEBUG))

    # redirect stdout and stderr to log files
    sys.stdout = get_logger('stdout_logger')
    sys.stderr = get_logger('stdout_logger')


def get_logger(name, host=''):
    global loggers
    if host:
        name += '.' + host
    if loggers.has_key(name):
        return loggers[name]
    return None


def create_text_logger(log_dir_base, log_name, basename='', host='',
                       backup_qty=10, stdout_level=None):
    if not tl_factory:
        return None
    logger = tl_factory.create(log_dir_base, log_name, basename, host,
                               backup_qty, stdout_level)
    return logger


def create_gui_logger(log_dir_base, log_name, dirname=None, host=''):
    if not gl_factory:
        return None
    logger = gl_factory.create(log_dir_base, log_name, dirname, host)
    return logger


def get_or_create_text_logger(log_dir_base, log_name, basename='', log_host='',
                              backup_qty=10, stdout_level=None):
    # Should be replaced with initialize_factories_if_neccesary decorator
    if not tl_factory:
        initialize_factories()

    logger = get_logger(log_name, log_host)
    if logger:
        return logger
    logger = tl_factory.create(log_dir_base, log_name, basename, log_host,
                               backup_qty, stdout_level)
    return logger


get_or_create_logger = get_or_create_text_logger  # alias


def get_or_create_gui_logger(log_dir_base, log_name, dirname='', log_host='',
                             stdout_level=None):
    # Should be replaced with initialize_factories_if_neccesary decorator
    if not gl_factory:
        initialize_factories()

    logger = get_logger(log_name, log_host)
    if logger:
        return logger
    logger = gl_factory.create(log_dir_base, log_name, dirname, log_host)
    return logger


def get_simple_logger(logger_name, log_dir=None, log_filename=None,
                      rollover_dir=False, backup_qty=10, stdout_level=None):
    """The only required parameter is the logger name. What's returned is a
        logger with a stdout handler. If log_dir and log_filename is specified,
        then a file handler is also added. An option is provided to rollover
        the log_dir instead of the log file. You can also specify the
        stdout_level.
    """
    global loggers
    logger = get_logger(logger_name, '')
    if logger:
        return logger

    global orig_stdout, logger_fmt, time_fmt
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # log everything by default

    # write to stdout
    hdlr = logging.StreamHandler(orig_stdout)
    hdlr.setFormatter(logging.Formatter(logger_fmt, time_fmt))
    logger.addHandler(hdlr)
    hdlr.setLevel(stdout_level or logging.INFO)

    # write to log file if so desired
    if log_dir and log_filename:
        # the option of rotating the log directory instead of the log file
        if rollover_dir:
            rollover_root_dir(log_dir, backup_qty)

        filename = os.path.normpath('/'.join((log_dir, log_filename)))

        file_obj = create_file_obj(filename, backup_qty=backup_qty)
        hdlr = logging.StreamHandler(file_obj)
        hdlr.setFormatter(logging.Formatter(logger_fmt, time_fmt))
        logger.addHandler(hdlr)

    # update global 'loggers' dictionary
    loggers[logger_name] = logger
    return logger

##################################
# END: LOGGER CREATOR/GETTERS
##################################
