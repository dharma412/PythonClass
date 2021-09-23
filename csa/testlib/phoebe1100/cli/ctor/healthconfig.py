#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/healthconfig.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

"""
SARF  CLI command: healthconfig
"""

import clictorbase
from clictorbase import REQUIRED, DEFAULT


class healthconfig(clictorbase.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln('healthconfig')
        return self

    def workqueue(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['edit_settings'] = ['edit the settings', DEFAULT]
        param_map['threshold_value'] = ['enter threshold', DEFAULT]
        param_map['receive_alerts'] = ['receive alerts', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('workqueue')
        return self._process_input(param_map)

    def cpu(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['edit_settings'] = ['edit the settings', DEFAULT]
        param_map['threshold_value'] = ['enter threshold', DEFAULT]
        param_map['receive_alerts'] = ['receive alerts', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('cpu')
        return self._process_input(param_map)

    def swap(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['edit_settings'] = ['edit the settings', DEFAULT]
        param_map['threshold_value'] = ['enter threshold', DEFAULT]
        param_map['receive_alerts'] = ['receive alerts', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('swap')
        return self._process_input(param_map)
