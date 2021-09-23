#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/graymailupdate.py#1 $
# $DateTime: 2019/06/27 23:26:24 $
# $Author: aminath $

import clictorbase as ccb
from sal.deprecated.expect import EXACT
from sal.containers.yesnodefault import is_yes


class graymailupdate(ccb.IafCliConfiguratorBase):

    def __call__(self, force=False):
        if is_yes(force):
            self._sess.writeln('graymailupdate force')
        else:
            self._sess.writeln('graymailupdate')

        exp_patterns = [
            ("Requesting check for new Graymail updates", EXACT),  # 1
            ("Requesting forced update for Graymail", EXACT),  # 2
            ("This feature is not enabled", EXACT),  # 3
            ("Updates are currently unavailable", EXACT),  # 4
        ]
        # Changed timeout to 15 because of non-error timeout issues
        self._expect(exp_patterns, timeout=15)
        self._wait_for_prompt()
        return exp_patterns[self._sess.expectindex][0]
