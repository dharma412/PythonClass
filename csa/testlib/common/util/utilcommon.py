#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/common/util/utilcommon.py#1 $

from common.logging import Logger
from common.arguments import ArgumentParser
from common.shell import shell
import sys


class UtilCommon(Logger, ArgumentParser):
    """Utilities Common class
    """

    # class level dictionary
    # all Util test libraries will work with single dictionary instance
    __shared_state = {}

    # default constructor required by UtilsLibrary
    def __init__(self, dut, dut_version):
        # dut info attributes
        self.dut = dut
        self.dut_version = dut_version

        if not UtilCommon.__shared_state.has_key(self.dut):
            self.start_shell_session()

    # RF Hybrid API for Test Libraries
    def get_keyword_names(self):
        return [
            'start_shell_session',
            'close_shell_session',
        ]

    # keywords
    def start_shell_session(self):
        try:
            self._shell = self._get_ironshell()
        except:
            self._shell = _NoShellSession()

    def close_shell_session(self):
        self._shell = _NoShellSession()

    # custom processing for _shell atrribute
    def __getattr__(self, name):
        if name == '_shell':
            return UtilCommon.__shared_state[self.dut]['ironshell']
        else:
            raise AttributeError("'%s' instance has no attribute '%s'" % \
                                 (self.__class__.__name__, name))

    def __setattr__(self, name, value):
        if name == '_shell':
            UtilCommon.__shared_state[self.dut] = {'ironshell': value}
        else:
            self.__dict__[name] = value

    def _get_ironshell(self):
        return shell.get_shell(self.dut, 'rtestuser', 'ironport')


class _NoShellSession():
    def __getattr__(self, name):
        raise RuntimeError('No Shell session is open')

    def __nonzero__(self):
        return False


def make_keyword(f):
    """"
    Source:
    http://code.activestate.com/recipes/576993-public-decorator-adds-an-item-to-__all__/

    Use a decorator to avoid retyping function/class names.

    * Based on an idea by Duncan Booth:
    http://groups.google.com/group/comp.lang.python/msg/11cbb03e09611b8a
    * Improved via a suggestion by Dave Angel:
    http://groups.google.com/group/comp.lang.python/msg/3d400fb22d8a42e1
    """
    kws = sys.modules[f.__module__].__dict__.setdefault('__keywords__', [])
    if f.__name__ not in kws:  # Prevent duplicates if run from an IDE.
        kws.append(f.__name__)
    return f
