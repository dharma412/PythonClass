#!/usr/bin/env python
"""
SARF 2 CLI command: servicelogsconfig
"""
import re

from sal.containers.yesnodefault import YES
from clictorbase import IafCliConfiguratorBase, IafCliParamMap, DEFAULT
from sal.exceptions import TimeoutError

class servicelogsconfig(IafCliConfiguratorBase):
    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def setup(self, share_stats=YES):
        self._query_response('setup')
        self._query_response(share_stats)
        # must say yes to either license agreement or
        # 'are you sure you want to turn this off?' question
        while 1:
            try:
                self._expect(['license agreement?', 'Are you sure','Choose the operation','-Press Any Key For More-'],timeout=20)
                if self._expectindex != 2:
		    if self._expectindex == 3:
		        self._writeln("\n")
		        continue
		    else:
		        self._query_response(YES)
		        self._to_the_top(1)
		else:
		    self._to_the_top(1)
		    break

            except TimeoutError:
                break


    def status(self):
        self._to_the_top(1)
        servicelogs_config_buffer_output = self.getbuf()
        self._debug(servicelogs_config_buffer_output)
        enabled_str = re.search('Share limited data with Service Logs Information Service: Enabled',\
                      servicelogs_config_buffer_output)
        if enabled_str:
            return 'Enabled'
        else:
            return 'Disabled'

    def fullsenderbaseconfig(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['max_sampling_rate'] = ['messages to be sampled for improving efficacy',\
                                         DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('FULLSENDERBASECONFIG')
        result = self._process_input(param_map, do_restart=False)
        self._to_the_top(1)
        return result

