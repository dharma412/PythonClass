#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/sieve_char.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class SieveChar(CliKeywordBase):
    """
    Sets or disables the character used for Sieve Email Filtering, as
    described in RFC 3598.  Note that the Sieve Character is ONLY
    recognized in LDAP Accept and LDAP Reroute queries and is ONLY
    applicable to the envelope-to address.  Other parts of the system
    will operate on the complete email address.

    Allowable characters are: -_=+/^#
    """

    def get_keyword_names(self):
        return ['sieve_char_setup']

    def sieve_char_setup(self, *args):
        """ Set the separator character.

        CLI command: sievechar > setup

        *Parameters:*
        - `char`: The Sieve Filter Character, or a space to disable Sieve Filtering.
        Allowable characters are: -_=+/^#

        *Return:*
        None

        *Examples:*
        | Sieve Char Setup | char=+ |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.sievechar().setup(**kwargs)
