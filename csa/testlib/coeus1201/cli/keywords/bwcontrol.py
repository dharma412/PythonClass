#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/bwcontrol.py#1 $ $DateTime: 2019/08/14 09:58:47 $ $Author: uvelayut $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class Bwcontrol(CliKeywordBase):
    """
    invoke Bandwidth control diagnostics tool from cli
    """

    def get_keyword_names(self):
        return [
                'bwcontrol_startlog',
                'bwcontrol_stoplog',
                'bwcontrol_listpipes',
                'bwcontrol_monitor',
            ]

    def bwcontrol_startlog(self ):
        """
        Enable logging of bandwidth control debug messages to proxylogs

        Parameters: None

        Examples:
            | BW Control Startlog |
        """
        return self._cli.simple_cli_command(command="bwcontrol startlog")

    def bwcontrol_stoplog(self ):
        """
        Disable logging of bandwidth control debug messages

        Parameters: None

        Examples:
            | BW Control Stoplog |
        """
        return self._cli.simple_cli_command(command="bwcontrol stoplog")

    def bwcontrol_listpipes(self ):
        """
        Display list of all bandwidth control pipes active on the WSA

        Parameters: None

        Examples:
            | BW Control Listpipes |
        """
        return self._cli.simple_cli_command(command="bwcontrol listpipes")

    def bwcontrol_monitor(self, pipe_number, break_timeout):
        """
        Display bandwidth measured for the given pipe, once every 5 seconds

        Parameters:
        - `pipe_number`: pipe_number to monitor
        - `break_timeout`: timeout in seconds after which monitoring should
        be stopped

        Examples:
            | BW Control Monitor | 3 | 30 |
        """
        return self._cli.simple_cli_command(
            command="bwcontrol monitor " + pipe_number,
            break_timeout=break_timeout
            )
