#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/smartagent_status_update.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class SmartagentStatusUpdate(CliKeywordBase):

    def get_keyword_names(self):
        return ['smart_agent_status',
                'smart_agent_update']

    def smart_agent_status(self):
        """
        Provides the details of smartagent version , and agent last updated info.

        smartlicenseagentstatus
        *Returns*:
         Dictionary with following component as keys:
         - 'Agent Version'
         - 'Last Updated'

         smartlicenseagentstatus displays below pattern of output:

         >smartlicenseagentstatus
         Component                 Version    Last Updated
         Smart License Agent       1.3.7      11 Dec 2017 10:08 (GMT +00:00)

         *Examples*:
         | ${Status}= | Smart Agent Status|
         ${Status} = {'Last Updated': 'Never updated', 'Agent Version': '1.3.7'}

         """
        return self._cli.smartagentstatus(smartagent="status").agent_status()

    def smart_agent_update(self):
        """
        Request updates for smartagent

        smartlicenseagentupdate
        *Returns*:
         None

        *Examples*:
        Smart Agent Update

        >smartlicenseagentupdate
        Requesting update of Smart License Agent.

        """
        return self._cli.smartagentstatus(smartagent="update")
