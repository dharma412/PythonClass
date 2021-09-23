#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/redirectrecipients.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

import clictorbase

DEFAULT = clictorbase.DEFAULT
REQUIRED = clictorbase.REQUIRED

class redirectrecipients(clictorbase.IafCliConfiguratorBase):

     def __call__(self, input_dict=None, **kwargs):
        self._writeln('redirectrecipients')
        param_map = clictorbase.IafCliParamMap(
                                    end_of_command=self._get_prompt())

        param_map['hostname'] = ['enter the hostname or IP address of the machine', REQUIRED]
        param_map['confirm']  = ['Are you sure you want to redirect all mail', DEFAULT]
        param_map.update(input_dict or kwargs)

        return self._process_input(param_map)

