#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/commit.py#1 $
"""IAF Command Line Interface (CLI) configurator: commit
"""

import clictorbase as ccb
from sal.exceptions import ConfigError


class commit(ccb.IafCliConfiguratorBase):

    def __call__(self, comments='IAF2 configurator', discard=ccb.DEFAULT, rollback=ccb.DEFAULT):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        idx = self._query('enter some comments describing your changes:',
                          'no data to commit.', timeout=120)
        if idx == 0:
            self._writeln(str(comments))
            idx = self._query('Are you ready to discard all of your changes?',
                              'save the current configuration for rollback',
                              self._get_prompt(), timeout=120)
            if idx == 0:
                self._writeln(discard)
                self._wait_for_prompt(timeout=120)
                return True
            elif idx == 1:
                self._writeln(rollback)
                self._wait_for_prompt(timeout=120)
                return True
            else:
                if discard != ccb.DEFAULT or rollback != ccb.DEFAULT:
                    raise ConfigError('Unanswered question')
        else:
            self._wait_for_prompt(timeout=120)
            return False
