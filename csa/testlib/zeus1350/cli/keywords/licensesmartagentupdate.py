#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/keywords/licensesmartagentupdate.py#1 $
# $DateTime: 2019/09/18 01:46:35 $
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
