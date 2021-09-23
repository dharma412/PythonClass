#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/licensesmartagentupdate.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

"""
  licensesmartagentupdate ctor
"""
import clictorbase as ccb

class licensesmartagentupdate(ccb.IafCliConfiguratorBase):
    def __call__(self, force = 'False'):
        if force:
            self._writeln('license_smart_agentupdate force')
            self._expect('Requesting forced update of Smart License Agent')
        else:
            self._writeln('license_smart_agentupdate')
            self._expect('Requesting update of Smart License Agent')
        return self
