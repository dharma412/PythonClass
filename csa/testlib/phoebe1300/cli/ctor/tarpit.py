#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/tarpit.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

"""
IAF 2 CLI command: tarpit
"""

import clictorbase
from clictorbase import DEFAULT, IafCliConfiguratorBase, IafCliParamMap
from sal.containers.yesnodefault import YES, NO


class tarpit(clictorbase.IafCliConfiguratorBase):

    def __call__(self):
        self._writeln('tarpit')
        return self

    def setup(self, input_dict=None, **kwargs):
        self._query_response('setup')

        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['slow_down'] = ['Should the system slow down', DEFAULT]
        param_map['memory_usage_for_rcmode'] = \
            ['memory usage required to enter', DEFAULT]
        param_map['memory_usage_to_refuse_mail'] = \
            ['memory usage required to refuse mail', DEFAULT]
        param_map['suspend_listener'] = \
            ['refuse mail by suspending listeners', DEFAULT]
        param_map['suspend_listener_on_work_queue_size'] = \
            ['suspend listeners based on work queue size', DEFAULT]
        param_map['no_of_msgs_to_suspend'] = \
            ['number of work queue messages', DEFAULT]
        param_map['no_of_msgs_to_resume'] = \
            ['messages at or below which listeners will be resumed', DEFAULT]
        param_map.update(input_dict or kwargs)
        return self._process_input(param_map)


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    tr = tarpit(cli_sess)
    tr().setup()
    tr().setup(suspend_listener=YES, memory_usage_for_rcmode=70,
               memory_usage_to_refuse_mail=80)
    tr().setup(suspend_listener=YES, suspend_listener_on_work_queue_size=YES,
               no_of_msgs_to_suspend=250, no_of_msgs_to_resume=10)
    tr().setup(suspend_listener=YES, suspend_listener_on_work_queue_size=NO)
