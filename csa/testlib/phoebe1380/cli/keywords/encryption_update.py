#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/keywords/encryption_update.py#1 $ $DateTime: 2020/01/06 01:25:43 $ $Author: saurgup5 $

from common.cli.clicommon import CliKeywordBase

class EncryptionUpdate(CliKeywordBase):
    """
    Fetch PXE Email Encryption updates.
    CLI command: encryptionupdate
    """
    def get_keyword_names(self):
        return ['encryption_update',]

    def encryption_update(self):
        """Fetch PXE Email Encryption updates.

        CLI command: encryptionupdate

        *Parameters:*
        None

        *Return:*
        Raw output.
        Possible response:\n
        _PXE Encryption not enabled. Engine not updated._\n
        _Requesting update of PXE Engine._

        *Examples:*
        | Encryption Update |
        """
        return self._cli.encryptionupdate()
