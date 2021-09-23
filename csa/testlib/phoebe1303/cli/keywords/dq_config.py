#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/dq_config.py#1 $
# $DateTime: 2020/01/17 04:04:23 $
# $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class DqConfig(CliKeywordBase):
    """
    This class provide keywords to configure Delayed Quarantine on ESA.
    Below is the flow of sdrconfig command:

     esa> dqconfig
          Space used: 0
          Numer of messages: 0
          Retention time: 1m


          Choose the operation you want to perform:
          - LISTMIDS - List MIDs of messages in the quarantine.
          - RELEASEMESSAGES - Release messages from quarantine.
          - MODIFYRETENTIONTIME - Modify retention timeout of quarantine.
          - DISABLEDQ - Disable Delayed Quarantine feature.

     esa>
    """

    def get_keyword_names(self):
        return ['dqconfig_is_enabled',
                'dqconfig_enable',
                'dqconfig_disable',
                'dqconfig_list_mids',
                'dqconfig_release_messages',
                'dqconfig_modify_retention_time']

    def dqconfig_is_enabled(self):
        """
        Keyword to check if Delayed Quarantine is enabled or not.

        :params:
            None
        :return:
            None
        :examples:
            | ${dq_status}= | Dqconfig Is Enabled |
        """
        return self._cli.dqconfig().is_enabled()

    def dqconfig_enable(self):
        """
        Keyword to enable Delayed Quarantine

        :params:

        :return:
            None
        :examples:
            | Dqconfig Enable |
        """
        self._cli.dqconfig().enable()

    def dqconfig_disable(self):
        """
        Keyword to disable Delayed Quarantine

        :params:
            None
        :return:
            None
        :examples:
            | Dqconfig Disable |
        """
        self._cli.dqconfig().disable()

    def dqconfig_list_mids(self):
        """
        Keyword to list MIDs in Quarantine

        :params:
            None
        :return:
            None
        :examples:
            | Dqconfig List Mids |
        """
        self._cli.dqconfig().list_mids()

    def dqconfig_release_messages(self):
        """
        Keyword to release messages in Quarantine

        :params:
            None
        :return:
            None
        :examples:
            | Dqconfig Release Messages |
        """
        self._cli.dqconfig().release_messages()

    def dqconfig_modify_retention_time(self, retention_time=60):
        """
        Keyword to modify quarantine retention time

        :params:
            None
        :return:
            None
        :examples:
            | Dqconfig Modify Retention Time |
        """
        self._cli.dqconfig().modify_retention_time(retention_time)

