#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/licensesmartagentstatus.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase

class licensesmartagentstatus(CliKeywordBase):

    def get_keyword_names(self):
        return ['license_smart_agent_status']

    def license_smart_agent_status(self):
        """
        Provides the details of smartagent version , and agent last updated info.

        license_smart_agentstatus
        *Returns*:
         Dictionary with following component as keys:
         - 'Agent Version'
         - 'Last Updated'

        license_smart_agentstatus displays below pattern of output:

        >license_smart_agentstatus
        Component                 Version    Last Updated
        Smart License Agent       1.3.7      11 Dec 2017 10:08 (GMT +00:00)

        *Examples*:
        | ${Status}= | License Smart Agent Status|
        ${Status} = {'Last Updated': 'Never updated', 'Agent Version': '1.3.7'}

        """
        return self._cli.licensesmartagentstatus().agent_status()
