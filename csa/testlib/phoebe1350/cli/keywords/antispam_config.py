#!/usr/bin/env python

from common.cli.clicommon import CliKeywordBase, DEFAULT

class AntispamConfig(CliKeywordBase):
    """
    cli -> antispamconfig

    antispamconfig
        Edit configuration for the following engines:
          IronPort Anti-Spam
          IronPort Intelligent Multi-Scan
          Symantec Brightmail Anti-Spam
          Cloudmark Service Provider Edition
    antispamconfig <enable|disable> bodyregex
        Edit Symantec Brightmail Anti-Spam body regex settings.
    antispamconfig <enable|disable> intsig
        Edit Symantec Brightmail Anti-Spam intsig settings.
    antispamconfig <enable|disable> usedfa
        Edit Symantec Brightmail Anti-Spam dfa settings.
    antispamconfig <status>
        View Symantec Brightmail Anti-Spam low-level config settings.

    """

    def get_keyword_names(self):
        return ['antispam_config_multiscan_setup',
                'antispam_config_brightmail_setup',
                'antispam_config_brightmail_tune',
                'antispam_config_case_setup',
                'antispam_config_cloudmark_setup'
                ]

    def antispam_config_multiscan_setup(self, *args):
        """
        This will edit the configuration of IronPort Intelligent Multi-Scan

        antispamconfig -> multiscan -> setup

        Parameters:
        - `use_ims` : use IronPort Intelligent Multi-Scan scanning.
                     Either 'yes' or 'no'
        - `scan_size` : largest size message that Intelligent Multi-Scan .
                      Add a trailing K for kilobytes, M for megabytes,
                       or no letters for bytes
        - `scan_timeout` : scanning timeout in secs
        - `reputation_filter_incoming` : Enable IP filtering for incoming messages
                                       Either 'yes' or 'no'
        - `reputation_filter_outgoing` : Enable IP filtering for outgoing messages
                                       Either 'yes' or 'no'
        - `region_scan` : Enable regional scanning. Either 'yes' or 'no'
        - `confirm_disable` : want to disable. Either 'yes' or 'no'
        - `choose_region` : Specify Region number  as per table
          | 1 | China |
        - `license_agreement` : accept agreement. Either 'yes' or 'no'
        - `mesg_larger_than` : Never scan message larger than.
                             Add a trailing K for kilobytes, M for megabytes,
                             or no letters for bytes
        - `mesg_smaller_than` : Always scan message smaller than.
                              Add a trailing K for kilobytes, M for megabytes,
                             or no letters for bytes

        Examples:

        | Antispam Config Multiscan Setup | use_ims=yes | mesg_smaller_than=1K |
        | Antispam Config Multiscan Setup | use_ims=no | confirm_disable=yes |

        """

        kwargs = self._convert_to_dict(args)
        self._cli.antispamconfig(vendor='multiscan').setup(**kwargs)

    def antispam_config_brightmail_setup(self, *args):
        """
        This will edit the configuration of Brightmail

        antispamconfig -> brightmail -> setup

        Parameters:
        - `use_bm` : use use Symantec Brightmail Anti-Spam scanning
                     Either 'yes' or 'no'
        - `spam_threshold` : Suspected Spam Threshold (between 25 and 89, or 100 to disable)
        - `use_reinsertion_key` : specify a reinsertion key for messages released from quarantine
                                Either 'yes' or 'no'
        - `reinsertion_key` : Enter Reinsertion key
        - `use_open_proxy_list` : Use Brightmail Anti-Spam Open Proxy List
                                 Either 'yes' or 'no'
        - `use_open_safe_list` : Use the Symantec Brightmail Anti-Spam Safe List
                                Either 'yes' or 'no'
        - `use_language_id` : Use Language Identification. Either 'yes' or 'no'
        - `max_msg_size` : Maximum size of message scanned by Symantec Brightmail Anti-Spam (in bytes)
        - `enable_caching` : cache verdicts for reuse on messages with an identical body
                            Either 'yes' or 'no'
        - `cache_duration` : how long to cache verdicts (in seconds)
        - `confirm_disable` : want to disable. Either 'yes' or 'no'
        - `license_agreement` : accept agreement. Either 'yes' or 'no'

        Examples:

        | Antispam Config Brightmail Setup | use_bm=yes | spam_threshold=75 |
        | Antispam Config Brightmail Setup | use_bm=no | confirm_disable=yes |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.antispamconfig(vendor='brightmail').setup(**kwargs)

    def antispam_config_brightmail_tune(self, *args):
        """
        This will set the number of servers for Brightmail Antispam

        antispamconfig -> brightmail -> tune

        Parameters:
        - `num_servers` : Number of servers. Default is 2

        Examples:
        | Antispam Config Brightmail Tune | num_servers=2 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.antispamconfig(vendor='brightmail').tune(**kwargs)

    def antispam_config_case_setup(self, *args):
        """
        This will edit the configuration of IronPort Antispam (Case)

        antispamconfig -> case -> setup

        Parameters:
        - `use_case` : use IronPort Antispam scan(case).
                     Either 'yes' or 'no'
        - `timeout` : scanning timeout in secs
        - `confirm_disable` : want to disable. Either 'yes' or 'no'
        - `license_agreement` : accept agreement. Either 'yes' or 'no'
        - `mesg_larger_than` : Never scan message larger than.
                             Add a trailing K for kilobytes, M for megabytes,
                             or no letters for bytes
        - `mesg_smaller_than` : Always scan message smaller than.
                              Add a trailing K for kilobytes, M for megabytes,
                             or no letters for bytes
        - `confirm_large` : confirm upper message size limit. Either 'yes' or 'no'
        - `confirm_small` : confirm lower message size limit. Either 'yes' or 'no'

        Examples:

        | Antispam Config Case Setup | use_case=yes | mesg_smaller_than=1K |
        | Antispam Config Case Setup | use_case=no | confirm_disable=yes |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.antispamconfig(vendor='ironport').setup(**kwargs)

    def antispam_config_cloudmark_setup(self, *args):
        """
        This will edit the configuration of Cloudmark Antispam

        antispamconfig -> cloudmark -> setup

        Parameters:
        - `use_cloudmark` : use Cloudmark Antispam.
                     Either 'yes' or 'no'
        - `max_msg_size` : Maximum message Size
        - `timeout` : scanning timeout in secs
        - `reputation_filter_incoming` : Enable IP filtering for incoming messages
                                       Either 'yes' or 'no'
        - `reputation_filter_outgoing` : Enable IP filtering for outgoing messages
                                       Either 'yes' or 'no'
        - `confirm_disable` : want to disable. Either 'yes' or 'no'
        - `license_agreement` : accept agreement. Either 'yes' or 'no'

        Examples:

        | Antispam Config Cloudmark Setup | use_ims=yes | mesg_smaller_than=1K |
        | Antispam Config Cloudmark Setup | use_ims=no | confirm_disable=yes |

        """
        kwargs = self._convert_to_dict(args)
        self._cli.antispamconfig(vendor='cloudmark').setup(**kwargs)

