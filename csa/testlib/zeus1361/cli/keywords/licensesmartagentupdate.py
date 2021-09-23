#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/keywords/licensesmartagentupdate.py#1 $
# $DateTime: 2020/03/05 19:45:32 $
# $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class licensesmartagentupdate(CliKeywordBase):

    def get_keyword_names(self):
        return ['license_smart_agent_update']

    def license_smart_agent_update(self, force):
        """
        Request updates for smartagent

        license_smart_agentupdate
        *Returns*:
         None

        *Examples*:
        License Smart Agent Update  force=True

        >license_smart_agentupdate force
        Requesting update of Smart License Agent.

        """
        self._cli.licensesmartagentupdate(force)
