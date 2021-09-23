#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/senderbaseconfig.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

"""
IAF 2 CLI command: senderbaseconfig
"""

from sal.containers.yesnodefault import YES
from clictorbase import IafCliConfiguratorBase, IafCliParamMap, DEFAULT


class senderbaseconfig(IafCliConfiguratorBase):
    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def setup(self, share_stats=YES):
        self._query_response('setup')
        self._query_response(share_stats)
        # must say yes to either license agreement or
        # 'are you sure you want to turn this off?' question
        idx = self._query('license agreement?', 'Are you sure',
                          'Choose the operation')
        if idx != 2:
            self._query_response(YES)
        self._to_the_top(1)

    def fullsenderbaseconfig(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['upload_host'] = ['SenderBase upload hostname', DEFAULT]
        param_map['upload_port'] = ['SenderBase upload port', DEFAULT]
        param_map['upload_freq'] = ['frequency to upload', DEFAULT]
        param_map['exclude_ip_stats'] = ['per-IP statistics', DEFAULT]
        param_map['max_sampling_rate'] = ['messages to be sampled for improving efficacy', \
                                          DEFAULT]
        param_map['max_ip'] = ['IP addresses to aggregate', DEFAULT]
        param_map['use_logging'] = ['verbose logging', DEFAULT]
        param_map['use_custom_lookup'] = ['configure a custom SenderBase', \
                                          DEFAULT]
        param_map['lookup_host'] = ['SenderBase Reputation lookup', DEFAULT]
        param_map['query_mode'] = ['mode of SenderBase query', DEFAULT]
        param_map['exclude_per'] = ['Exclude per-msg statistics', DEFAULT]
        param_map['max_msg'] = ['number of Messages to aggregate', DEFAULT]
        param_map['exclude_capacity'] = ['Exclude capacity statistics', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('FULLSENDERBASECONFIG')
        result = self._process_input(param_map, do_restart=False)
        self._to_the_top(1)
        return result
