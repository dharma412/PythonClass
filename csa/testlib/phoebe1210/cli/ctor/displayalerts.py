#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/displayalerts.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

"""
cli -> displayalerts

"""
from clictorbase import IafCliConfiguratorBase


class displayalerts(IafCliConfiguratorBase):

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._restart()
        self._writeln('displayalerts')
        alerts_status = self._wait_for_prompt()
        if 'There are no alerts stored currently on the appliance' in alerts_status:
            return 'There are no alerts stored currently on the appliance'
        return alerts_status
