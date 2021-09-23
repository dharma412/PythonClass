#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/keywords/set_host_name.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase


class SetHostName(CliKeywordBase):
    """Set the name of the machine."""

    def get_keyword_names(self):
        return ['set_host_name', ]

    def set_host_name(self, name):
        """Set the name of the machine.

        Parameters:
        - `name`: the new hostname for the machine.
        New name should match the following rules:
        - A label is a set of characters, numbers, dashes, and underscores.
        - The first and last character of a label must be a letter or a number.
        - The hostname must have at least 2 labels separated by a period.
        - The last label cannot be all numbers.


        Examples:
        | Set Host Name | newname.wga |

        | Set Host Name | wsa73.wga |
        """

        self._cli.sethostname(name)
