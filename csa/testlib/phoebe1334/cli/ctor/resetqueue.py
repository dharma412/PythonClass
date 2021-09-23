#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/resetqueue.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

import clictorbase
from sal.net.ping import wait_until_not_reachable
from sal.containers.yesnodefault import YES, NO

class resetqueue(clictorbase.IafCliConfiguratorBase):
    def __call__(self, confirm_continue=YES):

        self._writeln('resetqueue')

        if self._query('re you sure', self._sub_prompt) == 0:
            self._query_response(confirm_continue)
            if not confirm_continue:
                self._to_the_top(1)
                return

        wait_until_not_reachable(self.get_hostname(), 60)