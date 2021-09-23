#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/topin.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

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
