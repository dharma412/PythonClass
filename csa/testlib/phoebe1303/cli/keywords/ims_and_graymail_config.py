#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/ims_and_graymail_config.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase, DEFAULT
from sal.containers.yesnodefault import is_yes


class ImsAndGraymailConfig(CliKeywordBase):
    """
    imsandgraymailconfig

    Edit antispam engine settings.

    imsandgraymailconfig <engine> setup enable [options]
    imsandgraymailconfig <engine> setup disable
    imsandgraymailconfig globalconfig setup <commonoptions>

        engine  - Graymail Detection
            Engine to use.

        imsandgraymailconfig graymail setup enable [options]

        [options] - Various options to update graymail config parameters

             --unsubscription_enabled  Enable/Disable Safe Unsubscribe.
                                       Values: 0 for disable, 1 for enable

             --autoupdate_enabled      Enable/Disable automatic engine udpates.
                                       Values: 0 for disable, 1 for enable
        [commonoptions] - Various options to update the graymail and ims
                          common options
             --advisory_scan_size   Minimum message size to scan
                                    Values: Integer followed by K or M.
                                    Recommended setting is 512K or more.
                                    This is applicable only for ims

             --max_msg_size         Maximum message size to scan.
                                    Values: Integer followed by K or M.
                                    Recommended setting is 1024K(1MB) or less.

             --scan_timeout         Scan timeout.
                                    Default: 60 Range: 1-120
    """

    def get_keyword_names(self):
        return [
            'imsandgraymailconfig_graymail_setup',
            'imsandgraymailconfig_is_graymail_enabled',
            'imsandgraymailconfig_multiscan_setup',
            'imsandgraymailconfig_is_multiscan_enabled',
            'imsandgraymailconfig_globalconfig_setup',
        ]

    def imsandgraymailconfig_graymail_setup(self, *args):
        """
        This keyword will edit the configuration for the Graymail antispam engine.

        esa-admin-cli> imsandgraymailconfig

        Choose the operation you want to perform:
        - GRAYMAIL - Configure Graymail Detection and Safe Unsubscribe settings
        - MULTISCAN - Configure IronPort Intelligent Multi-Scan.
        - GLOBALCONFIG - Common Global Configuration settings
        []> graymail

        Graymail Detection: Disabled

        Choose the operation you want to perform:
        - SETUP - Configure Graymail.
        []> setup

        Would you like to use Graymail Detection? [Y]>

        Would you like to enable automatic updates for Graymail engine? [Y]>

        Graymail Safe Unsubscribe: Disabled
        Would you like to use Graymail Safe Unsubscribe? [Y]>

        Parameters:
            batch_mode - Parameter to execute imsandgraymailconfig -> graymail
                         command in batch mode. Values - Yes/No
            use_graymail_detection - Parameter to enable/disable graymaail. Values - Yes/No.
            enable_automatic_updates - Parameter to enable/disable auto-update. Values - Yes/No.
            use_graymail_safe_unsubscribe - Parameter to enable/disable safe unsubscribe. Values - Yes/No.
            license_agreement - Parameter to accept/decline graymail license.  Values - Yes/No.

        Examples:
            | Imsandgraymailconfig Graymail Setup       |
            | ... | use_graymail_detection=Yes          |
            | ... | enable_automatic_updates=Yes        |
            | ... | use_graymail_safe_unsubscribe=Yes   |

            | Imsandgraymailconfig Graymail Setup       |
            | ... | batch_mode=Yes                      |
            | ... | use_graymail_detection=Yes          |
            | ... | enable_automatic_updates=No         |
            | ... | use_graymail_safe_unsubscribe=No    |

            | Imsandgraymailconfig Graymail Setup       |
            | ... | batch_mode=Yes                      |
            | ... | use_graymail_detection=No           |
        """

        kwargs = self._convert_to_dict(args)
        batch_mode = True if 'batch_mode' in kwargs and is_yes(kwargs['batch_mode'].lower()) else False
        return self._cli.imsandgraymailconfig('GRAYMAIL', batch_mode).setup(**kwargs)

    def imsandgraymailconfig_is_graymail_enabled(self):
        """
        This keyword checks if Graymail engine is enabled or disabled. It executes the
        imsandgraymailconfig -> graymail command returns True or False based on the output.

        Parameters: None
        Return:     ${True} or ${False}

        Examples:
            |  ${gm_status}=        |  Imsandgraymailconfig Is Graymail Enabled   |
            |  Should Not Be True   | ${gm_status}                                  |
        """

        return self._cli.imsandgraymailconfig('GRAYMAIL').is_enabled()

    def imsandgraymailconfig_multiscan_setup(self, *args):
        """
        This keyword will edit the configuration for the Ironport Multi-Scan antispam engine.

        esa-admin-cli> imsandgraymailconfig

        Choose the operation you want to perform:
        - GRAYMAIL - Configure Graymail Detection and Safe Unsubscribe settings
        - MULTISCAN - Configure IronPort Intelligent Multi-Scan.
        - GLOBALCONFIG - Common Global Configuration settings
        []> multiscan

        IronPort Intelligent Multi-Scan: Disabled


        Choose the operation you want to perform:
        - SETUP - Edit Intelligent Multi-Scan settings.
        []> setup

        IronPort Intelligent Multi-Scan scanning: Disabled
        Would you like to use IronPort Intelligent Multi-Scan scanning? [Y]>

        Would you like to enable regional scanning? [N]>

        Parameters:
            use_ims_scanning -
            confirm_disable -
            enable_regional_scanning -
            region -
            license_agreement -

        Return: None

        Examples:
            |  Imsandgraymailconfig Multiscan Setup   |
            |  ...  |  use_ims_scanning=Yes             |
            |  ...  |  enable_regional_scanning=Yes     |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.imsandgraymailconfig('MULTISCAN').setup(**kwargs)

    def imsandgraymailconfig_is_multiscan_enabled(self):
        """
        This keyword checks if Ironport Intelligent Multi-Scan engine is enabled or disabled.
        It executes the imsandgraymailconfig -> multiscan command returns True or False based
        on the output.

        Parameters: None
        Return:     ${True} or ${False}

        Examples:
            |  ${gm_status}=    |  Imsandgraymailconfig Is Multiscan Enabled  |
            |  Should Be True   | ${gm_status}                                  |
        """
        return self._cli.imsandgraymailconfig('MULTISCAN').is_enabled()

    def imsandgraymailconfig_globalconfig_setup(self, *args):
        """
        This keyword edits the global configuration common to both Graymail and IMS engine.

        esa-admin-cli> imsandgraymailconfig

        Choose the operation you want to perform:
        - GRAYMAIL - Configure Graymail Detection and Safe Unsubscribe settings
        - MULTISCAN - Configure IronPort Intelligent Multi-Scan.
        - GLOBALCONFIG - Common Global Configuration settings
        []> globalconfig

        Choose the operation you want to perform:
        - SETUP - Configure Common Global settings
        []> setup

        Increasing the following size settings may result in decreased performance. Please consult
        documentation for size recommendations based on your environment.

        Never scan message larger than: (Add a trailing K for kilobytes, M for megabytes, or
        no letters for bytes.)
        [1M]>

        Always scan message smaller than: (Add a trailing K for kilobytes, M for megabytes, or
        no letters for bytes.)
        [512K]>

        Timeout for Scanning Single Message(in seconds):
        [60]>

        Parameters:
            batch_mode - Parameter to execute imsandgraymailconfig -> globalconfig
                         command in batch mode. Value - Yes/No
            dont_scan_message_larger_than - Maximum message size for scanning. Eg: 2M/256K
            confirm_message_scanning_size - Confirm changing message scanning size
                                            beyond recommended values. Default: No
            re_enter_message_scanning_size - Re-enter message scanning size after
                                             warning. Deafult: 1M
            always_scan_message_smaller_than - Minimum message size for scanning. Eg: 100K/1M
            single_message_scanning_timeout - Timeout for scanning a single message (in seconds)

        Return: None

        Examples:
            |  Imsandgraymailconfig Globalconfig Setup      |
            |  ...  |  dont_scan_message_larger_than=2M     |
            |  ...  |  always_scan_message_smaller_than=1M  |
            |  ...  |  single_message_scanning_timeout=120  |

            |  Imsandgraymailconfig Globalconfig Setup      |
            |  ...  |  batch_mode=Yes                       |
            |  ...  |  dont_scan_message_larger_than=5M     |
            |  ...  |  always_scan_message_smaller_than=2M  |
            |  ...  |  single_message_scanning_timeout=90   |

            |  Imsandgraymailconfig Globalconfig Setup      |
            |  ...  |  batch_mode=Yes                       |
            |  ...  |  always_scan_message_smaller_than=10K |
            |  ...  |  single_message_scanning_timeout=100  |
        """
        kwargs = self._convert_to_dict(args)
        batch_mode = True if 'batch_mode' in kwargs and is_yes(kwargs['batch_mode'].lower()) else False
        return self._cli.imsandgraymailconfig('GLOBALCONFIG', batch_mode).setup(**kwargs)
