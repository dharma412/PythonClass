#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/test_ntlm_auth.py#1 $

from common.cli.clicommon import CliKeywordBase, DEFAULT

class TestNtlmAuth(CliKeywordBase):
    """Performs interactive ntlm authentication based on NTLM Message-1,
       Message-2, Message-3
    """

    def get_keyword_names(self):
        return [
                'test_ntlm_auth'
               ]

    def test_ntlm_auth(self, msg_1, msg_2, msg_3):
        """Performs interactive ntlm authentication based on NTLM Message-1,
           Message-2, Message-3.  Please refer to this doc:
           http://davenport.sourceforge.net/ntlm.html for explanation of these
           different type of messages.

        Parameters:
           - `msg_1`: NTLM Type 1 message.
           - `msg_2`: NTLM Type 2 message.
           - `msg_3`: NTLM Type 3 message.

        Example:
        | Test NTLM Auth | TlRMTVNTUAABAAAABo= |
        | | TlRMTVNTUAACAAAADAAMADAAAAAGgokAYpHp/DrASScAAAAAAAAAAE4ATgA8AAAA |
        | | TlRMTVNTUAADAAAAGAAYAEAAAAAYABgAWAAAABAAEABwAAAABwAHAIAAAAAPAA8A'hwAAAAAAAAAAAAAABoKJAJSx+5yC4dFjAAAAAAAAAAAAAAAAAAAAAPO75kquEsDEa |
        """
        return self._cli.testntlmauth(msg_1, msg_2, msg_3)
