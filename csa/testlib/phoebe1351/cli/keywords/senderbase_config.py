#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/senderbase_config.py#2 $ $DateTime: 2020/01/17 04:04:23 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase

class SenderBaseConfig(CliKeywordBase):
    """
    Manage Sender Base configuration.
    CLI command: senderbaseconfig
    """

    def get_keyword_names(self):
        return ['senderbase_config_setup',
                'senderbase_config_full',
                'senderbase_config_status']

    def senderbase_config_setup(self, *args):
        """Setup senderbase config

        CLI command: senderbaseconfig > setup

        *Parameters:*
        - `share_stats`: Share limited data with SenderBase Information Service.
                         YES or NO.

        *Return:*
        None

        *Examples:*
        | Senderbase Config Setup | share_stats=yes |
        | Senderbase Config Setup | share_stats=no |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.senderbaseconfig().setup(**kwargs)

    def senderbase_config_full(self, *args):
        """fullsenderbaseconfig hidden command

        CLI command: senderbaseconfig > fullsenderbaseconfig
        Note: _fullsenderbaseconfig_ is a hidden sub-command.

        *Parameters:*
        - `upload_host`: SenderBase upload hostname. String. Optional.
        - `upload_port`: SenderBase upload port. String. Optional.
        - `upload_freq`: the frequency to upload information (in seconds).
                         String. Optional.
        - `exclude_ip_stats`: Exclude per-IP statistics. YES or NO.
                              NO by default.
        - `use_logging`: Enable verbose logging at the TRACE level. YES or NO.
                         NO by default.
        - `max_sampling_rate`: Enter the maximum rate of sampling messages for
                               improved efficacy (value in percent upto two
                               places after decimal point)
        - `max_ip`: The maximum number of IP addresses to aggregate. String.
                    Optional.
        - `use_custom_lookup`: Configure a custom SenderBase lookup. YES or NO.
                               NO by default.
        - `lookup_host`: The SenderBase Reputation lookup host. String. Required
        - `query_mode`:  The mode of SenderBase query. String. Optional.
        The SenderBase query mode may be:
        _'norm'_, _'pasv'_, or _'compat'_

        *Return:*
        None

        *Examples:*
        | Senderbase Config Setup | share_stats=yes |

        | Senderbase Config Setup | share_stats=n |

        | Senderbase Config Full |
        | ... | upload_host=my.sender.base.qa |
        | ... | upload_port=8888 |
        | ... | upload_freq=3600 |
        | ... | exclude_ip_stats=no |
        | ... | max_ip=5000 |
        | ... | max_sampling_rate=7.05 |
        | ... | use_logging=y |
        | ... | use_custom_lookup=yes |
        | ... | lookup_host=rep.host.qa |
        | ... | query_mode=compat |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.senderbaseconfig().fullsenderbaseconfig(**kwargs)

    def senderbase_config_status(self):
        """This keyword to get the current status of the sender base config
        *Return:*
        Enabled or Disabled
        *Examples:*
        $status=    |SenderBase Config Status|
        """
        return self._cli.senderbaseconfig().status()
