#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/addressconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $
"""
CLI command addressconfig
"""

from sal.containers.yesnodefault import YES, NO
import clictorbase
from clictorbase import DEFAULT


class addressconfig(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def addressconfig_edit(self, oper, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(
            end_of_command='Choose the operation')
        param_map['display_name'] = ['enter the display name portion',
                                     DEFAULT]
        param_map['user_name'] = ['enter the user name portion', DEFAULT]
        param_map['use_hostname'] = \
            ['use the system hostname for the domain portion?',
             DEFAULT]
        param_map['domain_name'] = \
            ['enter the domain name portion of the', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response(oper)
        return self._process_input(param_map)
