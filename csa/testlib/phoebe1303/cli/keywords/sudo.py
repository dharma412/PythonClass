#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/sudo.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase

class Sudo(CliKeywordBase):
    """
    Run an IronPort support command.

    CLI command: sudo
    """

    def get_keyword_names(self):
        return ['sudo',]

    def sudo(self, *args):
        """Run an IronPort support command.

        CLI command: sudo

        *Parameters:*
        - `cmd`: Support command.
        To get list of allowed commands.
        cat _/usr/local/etc/sudoers_
        * _ifconfig_
        * _netstat_
        * _ps_
        * _top_
        * _ts_
        - `password`: Support user password.
        By default it is _1psupp0rt_.
        - `need_interrupt`: Command needs manual interrupt(like _top_). YES or NO.
        - `interrupt_interval`: Time in seconds to wait before interruption.

        *Return:*
        Raw output.

        *Examples:*
        | ${top}= | Sudo |
        | ... | cmd=top |
        | ... | password=1psupp0rt |
        | ... | need_interrupt=yes |
        | ... | interrupt_interval=10 |
        | Log | ${top} |

        | ${interfaces}= | Sudo |
        | ... | cmd=ifconfig |
        | ... | password=1psupp0rt |
        | Log | ${interfaces} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.sudo(**kwargs)