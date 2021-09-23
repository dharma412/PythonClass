#!/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/displayalerts.py#1 $
# $DateTime: 2019/06/27 23:26:24 $
# $Author: aminath $

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
