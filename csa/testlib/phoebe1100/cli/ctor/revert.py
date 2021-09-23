#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/revert.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $
"""
IAF2 CLI command revert
"""
import re

import clictorbase

from sal.containers.yesnodefault import YES, NO
from common.cli.clicommon import CliKeywordBase

REQUIRED = clictorbase.REQUIRED


class revert(clictorbase.IafCliConfiguratorBase):

    def __call__(self, input_dict=None, **kwargs):
        self._writeln(self.__class__.__name__)

        end_criteria = '(%s)|(%s)' % (self._get_prompt().single, 'The system will now reboot')
        param_map = clictorbase.IafCliParamMap(end_of_command=re.compile(end_criteria))
        param_map['version'] = ['select an AsyncOS version', REQUIRED, True]
        param_map['continue'] = ['Do you want to continue', NO]
        param_map['confirm'] = ['sure you want to continue', NO]
        param_map['confirm_switch'] = ['restricted to run in machine mode', YES]
        param_map.update(input_dict or kwargs)

        self._process_input(param_map, do_restart=False)

        try:
            self._restart()
        except:
            pass
