#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/sdr_config.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase


class SdrConfig(CliKeywordBase):
    """This class provide keywords to configure Sender Domain Reputation on ESA.
       Below is the flow of sdrconfig command:

     esa> sdrconfig
     Would you like to disable sender domain reputation check? [N]>
     The following additional attributes of the message can also be included in the Sender Domain Reputation check to improve the efficacy:
    1. Name part of the From and Reply to headers.
    2. Display fields of the From and Reply to headers.
    Do you want to include these additional attributes of the message for the Sender Domain Reputation check? [Y]>

     esa>
    """

    def get_keyword_names(self):
        return ['sdrconfig_is_enabled',
                'sdrconfig_enable',
                'sdrconfig_disable',
                'sdrconfig_edit',
                'sdrconfig_batch']

    def sdrconfig_is_enabled(self):
        """
        Keyword to check if sender domain reputation is enabled or not.

        :params:
            None
        :return:
            None
        :examples:
            | ${sdr_status}= | Sdrconfig Is Enabled |
        """
        return self._cli.sdrconfig.is_enabled()

    def sdrconfig_enable(self, include_additional_attributes='Y'):
        """
        Keyword to enable sender domain reputation.

        :params:
            include_additional_attributes: Y/N. Default - Y
        :return:
            None
        :examples:
            | ${sdr_status}= | Sdrconfig Enable
            | ${sdr_status}= |  Sdrconfig Enable | include_additional_attributes=Y |
        """
        self._cli.sdrconfig.enable(include_additional_attributes)

    def sdrconfig_disable(self):
        """
        Keyword to disable sender domain reputation.

        :params:
            None
        :return:
            None
        :examples:
            | ${sdr_status}= | Sdrconfig Disabled |
        """
        self._cli.sdrconfig.disable()

    def sdrconfig_edit(self, include_additional_attributes='Y'):
        """
        Keyword to edit sender domain reputation settings.

        :params:
            include_additional_attributes: Y/N. Default - Y
        :return:
            None
        :examples:
            | ${sdr_status}= | Sdrconfig Edit | include_additional_attributes=N |
        """
        self._cli.sdrconfig.edit(include_additional_attributes)

    def sdrconfig_batch(self, *args):
        """
        Keyword to run sdrconfig command in batch mode.

        :params:
            action: Enable or Disable
            share_extended_info: Enable or Disable
        :return:
            None
        :examples:
            | Sdrconfig Batch | action=Enable | share_extended_info=Disable |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.sdrconfig.batch(**kwargs)