#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/resume_del.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class ResumeDel(CliKeywordBase):
    """Keywords for resumedel CLI command."""

    def get_keyword_names(self):
        return ['resumedel', ]

    def resumedel(self, domain_str='ALL'):
        """Resume delivery.

        *Parameters:*
        | - `domain_str` | one or more domains [comma-separated] to which you want to suspend delivery |
        |                | The following formats are allowed: |
        |                | - Hostnames such as "example.com", "[1.2.3.4]", "[2001:420:80:1::5]" |
        |                | - Partial hostnames such as ".example.com" |

        | If no parameter provided, the default will be applied : domain_str=ALL |

        Exceptions:
        - `ConfigError`: in case delivery can not be resumed.

        *Examples:*
        | Resume Del |
        | Resume Del | test.com, 192.168.1.1, .voffka.com, [2001:420:80:1::5] |
        """
        self._cli.resumedel(domain_str)
