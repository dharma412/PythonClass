#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/licensesmartagentupdate.py#1 $
# $DateTime: 2019/06/27 23:26:24 $
# $Author: aminath $

"""
  licensesmartagentupdate ctor
"""
import clictorbase as ccb


class licensesmartagentupdate(ccb.IafCliConfiguratorBase):
    def __call__(self, force='False'):
        if force:
            self._writeln('license_smart_agentupdate force')
            self._expect('Requesting forced update of Smart License Agent')
        else:
            self._writeln('license_smart_agentupdate')
            self._expect('Requesting update of Smart License Agent')
        return self
