#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/tuistatus.py#1 $

"""
CLI command: tuistatus
"""
from sal.exceptions import ConfigError
import clictorbase as ccb
from sal.deprecated.expect import EXACT, REGEX

from clictorbase import IafCliConfiguratorBase, IafCliError


class tuistatus(IafCliConfiguratorBase):

    def __call__(self):
        self.clearbuf()
        self._writeln('tuistatus')
        return self

    def adagentstatus(self):
        self._writeln('ADAGENTSTATUS')
        self._to_the_top(1)
        out = self.getbuf()
        return out

    def listlocalmappings(self):
        self._writeln('LISTLOCALMAPPINGS')
        self._to_the_top(1)
        out = self.getbuf()
        return out

