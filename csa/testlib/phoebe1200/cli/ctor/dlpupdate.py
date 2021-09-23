#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/dlpupdate.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

"""
CLI command - dlpupdate
"""

import clictorbase as ccb
from sal.deprecated.expect import EXACT, REGEX
from sal.containers.yesnodefault import is_yes, is_no
from sal.containers.cfgholder import CfgHolder
import re

pats = [
    ("DLP should be enabled to run updates", REGEX),
    ("Checking for available updates.", REGEX),
    ("Forcing update of DLP Engine", EXACT),
]

setup_pats = [
    ("Automatic updates for DLP are enabled", REGEX),
    ("Automatic updates for DLP are disabled", REGEX),
]


class dlpupdate(ccb.IafCliConfiguratorBase):

    def __call__(self, force=False, self_hook=False):
        self.clearbuf()
        if force or is_yes(force):
            self._sess.writeln('dlpupdate force')
            self._expect(pats, timeout=15)
            self._wait_for_prompt()
            return pats[self._sess.expectindex][0]
        self._sess.writeln('dlpupdate')
        self._expect(pats, timeout=15)
        if self._sess.expectindex == 0:
            self._wait_for_prompt()
            return pats[self._sess.expectindex][0]
        elif self._sess.expectindex == 1:
            if self_hook:
                return self
            self._to_the_top(1)
            return pats[self._sess.expectindex][0]

    def setup(self, enable_auto_update=None):
        self._sess.writeln('SETUP')
        self._expect(setup_pats, timeout=15)
        if self._sess.expectindex == 0 and is_no(enable_auto_update):
            self._query_response(enable_auto_update)
        if self._sess.expectindex == 1 and is_yes(enable_auto_update):
            self._query_response(enable_auto_update)
        self._to_the_top(2)

    def is_enabled(self):
        self._sess.writeln('SETUP')
        self._expect(setup_pats, timeout=15)
        self._to_the_top(2)
        if self._sess.expectindex == 0:
            return True
        if self._sess.expectindex == 1:
            return False
