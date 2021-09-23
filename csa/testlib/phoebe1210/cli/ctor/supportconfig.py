#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/supportconfig.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

"""
SARF CLI command: supportconfig
"""

import clictorbase

from clictorbase import IafCliConfiguratorBase, IafCliParamMap, DEFAULT


class supportconfig(IafCliConfiguratorBase):

    def __call__(self, input_dict=None, **kwargs):
        self._writeln(self.__class__.__name__)
        return self

    def supportrequest(self, input_dict=None, **kwargs):
        param_map = \
            IafCliParamMap(end_of_command='NOTE: Changes to support')

        self._query_response('SUPPORTREQUEST')
        param_map['email'] = \
            ['Enter the destination email', DEFAULT]
        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)
