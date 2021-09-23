#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/revert.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $
"""
SARF CLI command revert
"""
import re
from sal.containers.yesnodefault import YES, NO
from sal.exceptions import ExpectError

import clictorbase

REQUIRED = clictorbase.REQUIRED


class revert(clictorbase.IafCliConfiguratorBase):

    def __call__(self, input_dict=None, **kwargs):
        self._writeln(self.__class__.__name__)

        end_criteria = '(%s)|(%s)' % (self._get_prompt().single,
                                      'The system will now reboot')
        param_map = clictorbase.IafCliParamMap(
            end_of_command=re.compile(end_criteria))
        param_map['version'] = ['select an AsyncOS version', REQUIRED, True]
        param_map['continue'] = ['Do you want to continue', NO]
        param_map['confirm'] = ['sure you want to continue', NO]
        param_map['confirm_switch'] = ['restricted to run in machine mode', YES]
        param_map.update(input_dict or kwargs)

        try:
            self._process_input(param_map)
        except ExpectError:
            print '** DEBUG ** Revert process started. CLI connection broken'
            print self.getbuf()
            pass
        except Exception as e:
            print '** ERROR ** FAILURE occured in revert command'
            print self.getbuf()
            raise e
