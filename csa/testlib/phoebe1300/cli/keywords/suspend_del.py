#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/suspend_del.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class SuspendDel(CliKeywordBase):
    """Keywords for suspenddel CLI command."""

    def get_keyword_names(self):
        return ['suspend_del', ]

    def suspend_del(self, delay=None, domain_str='ALL'):
        """Suspend delivery.

        *Parameters:*
        | - `delay` | maximum number of seconds to wait for connections to close |
        |           | before doing a forceful disconnect. |
        | - `domain_str` | one or more domains [comma-separated] to which you want to suspend delivery |
        |                | The following formats are allowed: |
        |                | - Hostnames such as "example.com", "[1.2.3.4]", "[2001:420:80:1::5]" |
        |                | - Partial hostnames such as ".example.com" |

        | If no parameter provided, the default will be applied : delay=30, domain_str=ALL |

        *Examples:*
        | Suspend Del |
        | Suspend Del | 10 | test.com, 192.168.1.1, .voffka.com, [2001:420:80:1::5] |
        """
        self._cli.suspenddel(delay, domain_str)
