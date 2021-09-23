#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/domain_rep_config.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase


class DomainRepConfig(CliKeywordBase):
    """This class provide keywords to configure Domain Reputation Config on ESA.
       Below is the flow of domainrepconfig command:

     esa> domainrepconfig

     Would you like to configure an exception list for Sender Domain Reputation and External Threat Feeds functionality? [Y]>

     Select the domain only address list to to be used for Sender Domain Reputation and External Threat Feeds functionality
     1. domain_exception_list
     [1]>
     esa>
    """

    def get_keyword_names(self):
        return ['domain_rep_config_enable',
                'domain_rep_config_disable',
                'domain_rep_config_batch']

    def domain_rep_config_enable(self, *args):
        """
        Keyword to enable domain reputation config

        :params:
            domain_exception_list: Pass the excepted domain address list name
        :return:
            None
        :examples:
            | Domain Rep Config Enable                      |
            | ... | domain_exception_list=test_address_list |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainrepconfig().enable(**kwargs)

    def domain_rep_config_disable(self):
        """
        Keyword to disable domain reputation config

        :params:
            None
        :return:
            None
        :examples:
            | Domain Rep Config Disable |
        """
        self._cli.domainrepconfig().disable()

    def domain_rep_config_batch(self, *args):
        """
        Keyword to run domain reputation config command in batch mode

        :params:
            domain_exception_list: Pass the excepted domain address list name
        :return:
            None
        :examples:
            | Domain Rep Config Batch                       |
            | ... | domain_exception_list=test_address_list |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.domainrepconfig.batch(**kwargs)