#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/outbreak_config.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

"""
SARF CLI command: outbreakconfig
"""

from common.cli.clicommon import CliKeywordBase

class OutbreakConfig(CliKeywordBase):
    """
    Setup Outbreak Filters settings.

    CLI command: outbreakconfig
    """

    def get_keyword_names(self):
        return ['outbreak_config_setup',
                'outbreak_config_proxyconfig',
                'outbreak_config',]

    def outbreak_config_setup(self, *args):
        """Change Outbreak Filters settings.

        CLI command: outbreakconfig > setup

        *Parameters:*
        - `use`: Use Outbreak Filters. YES or NO.
        - `disable`: Disable outbreak filters. YES or NO.
        - `alerts`: Receive Outbreak Filter alerts. YES or NO.
        - `max_message_size`: The largest size message Outbreak Filters should scan. Optional.
        - `use_heuristics`: Use adaptive rules to compute the threat level of messages. YES or NO.
        - `log_urls`: Enable Logging of URL's. YES or NO.
        - `enable_urlclick_tracking`: Enable URL Click Tracking. YES or NO.
        - `disable_urlclick_tracking`: Disable URL Click Tracking. YES or NO.
        - `agreement`: Accept license agreement. YES or NO.

        *Return:*
        None

        *Examples:*
        | Outbreak Config Setup |
        | ... | use=y |
        | ... | alerts=yes |
        | ... | max_message_size=10000000 |
        | ... | use_heuristics=yes |
        | ... | log_urls=yes |
        | ... | enable_urlclick_tracking=yes |

        | Outbreak Config Setup |
        | ... | use=no |
        | ... | disable=yes |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.outbreakconfig().setup(**kwargs)

    def outbreak_config_proxyconfig(self, *args):
        """Change Outbreak Filters ProxyConfig settings.

        CLI command: outbreakconfig > proxyconfig

        *Parameters:*
        - `proxy_template`: Change Outbreak Filters proxy template. OPTIONAL
        - `proxy_key`: Change Outbreak Filters proxy key. OPTIONAL

        *Return:*
        None

        *Examples:*
        | Outbreak Config Proxyconfig |
        | ... | proxy_template=cisco.com |
        | ... | proxy_key=cisco |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.outbreakconfig().proxyconfig(**kwargs)

    def outbreak_config(self, *args):
        """Change Outbreak Filters settings in batch mode.

        CLI command: outbreakconfig

        *Parameters:*
        - `option`: Option(s) for batch mode.
        Options for batch mode:
        | enable |
        | disable |
        | tag-only | _on_ or _off_ |
        | rescan | _on_ or _off_ |
        | threshold | one from _1_, _2_, _3_, _4_, _5_ |
        | alerts | _enable_ or _disable_ |
        | timeout | value from _1_ to _120_ |

        *Return:*
        None

        *Examples:*
        | Outbreak Config |
        | ... | option=timeout 60 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.outbreakconfig(**kwargs)