#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/licensesmartagentupdate.py#3 $
# $DateTime: 2019/06/07 02:45:52 $
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
