#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/clustermode.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import re
import clictorbase
from clictorbase import DEFAULT, NO_DEFAULT, REQUIRED
from sal.containers.yesnodefault import YES, NO


class clustermode(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

        # errors that can appear in __call__()
        __call__clustermode_error_strings = (
            'command requires a feature key',
            'command is only available on cluster system',
            'not yet resynchronized with the cluster after upgrading'
        )
        err_dict = {}
        for err_str in __call__clustermode_error_strings:
            err_dict[(err_str, clictorbase.EXACT)] = clictorbase.IafCliError
        self._set_local_err_dict(err_dict)

    def __call__(self, level=DEFAULT, machine_or_group_name=DEFAULT):
        # level: 'cluster', 'group', 'machine', ''

        assert level in ('cluster', 'group', 'machine', ''), \
            'unknown level:%s' % level
        self._writeln('clustermode')
        if level:
            level = level.capitalize()

        self._query('Choose the configuration')
        self._query_select_list_item(level)

        if self._query('Choose', self._get_prompt()) == 0:
            # Questions: "Choose the group to configure." or "Choose a machine."
            self._query_select_list_item(machine_or_group_name)
            self._wait_for_prompt()
        # else: prompt already gotten


if __name__ == '__main__':
    sess = clictorbase.get_sess()
    cm = clustermode(sess)
    cm('cluster')
    cm('group', '1')
    cm('group', 'Main_Group')
    cm('machine', '1')

    # If a 2nd cluster group exists in the cluster
    multi_group = False
    if multi_group:
        group_name = 'iafgroup'
        cm('group', '2')
        cm('group', group_name)

    # If a 2nd MGA exist in the cluster
    multi_machine = False
    if multi_machine:
        machine_name1 = 'cinnamon.qa'
        machine_name2 = 'tim.qa'

        cm('machine', machine_name1)
        cm('machine', '2')
        cm('machine', machine_name2)
