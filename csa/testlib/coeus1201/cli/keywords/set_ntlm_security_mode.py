#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/set_ntlm_security_mode.py#1 $

from common.cli.clicommon import CliKeywordBase

class SetNtlmSecurityMode(CliKeywordBase):
    """Configures the security mode used while joining to the Active Directory server."""

    def get_keyword_names(self):
        return ['set_ntlm_security_mode']

    def set_ntlm_security_mode(self, mode=None):
        """Set NTLM Security Mode.

        Parameters:
        - `mode`: string with mode value. Either 'domain' or 'ads'.

        Examples:
        | Set NTLM Security Mode | mode=ads |
        | Set NTLM Security Mode | mode=domain |
        """
        modes = {'ads': 1, 'domain': 2}
        if mode.strip().lower() in modes.keys():
            self._cli.setntlmsecuritymode(modes[mode])
        else:
            raise ValueError('Mode must be domain or ads.')