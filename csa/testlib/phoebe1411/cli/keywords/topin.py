#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/topin.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import (CliKeywordBase, DEFAULT)

class Topin(CliKeywordBase):

    """Keywords for topin CLI command."""

    def get_keyword_names(self):
        return ['topin',
                ]

    def topin(self):
        """
        Display the top hosts by number of incoming connections.

        *Parameters:*
        None.

        *Return:*
        Output of command.

        *Exceptons:*
        None.

        *Examples:*
        | ${out} | Topin |
        """
        return self._cli.topin()

