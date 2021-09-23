#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/encryption_status.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class EncryptionStatus(CliKeywordBase):
    """
    Fetch PXE Email Encryption status.
    CLI command: encryptionstatus
    """

    def get_keyword_names(self):
        return ['encryption_status', ]

    def encryption_status(self, *args):
        """Enable/Disable IronPort Email Encryption.

        CLI command: encryptionstatus

        *Parameters:*
        - `as_dictionary`: Return result formatted as dictionary. YES or NO.

        *Return:*
        Dictionary or raw output.
        Dictionary has the following keys which are dictionaries themselves:
        - _pxe_engine_
        - _domain_mapping_

        Each of them has keys:
        - _version_
        - _last_updated_

        _Example_:\n
        {'pxe_engine': {'version': '6.9.0-009',
                        'last_updated': '19 Jul 2012 00:18 (GMT +00:00)\r'},
        'domain_mapping': {'version': '1.0.0',
                           'last_updated': 'Never updated\r'}}

        *Examples:*
        | Encryption Status | as_dictionary=y |
        | Encryption Status | as_dictionary=n |

        | ${res}= | Encryption Status |
        | ${engine}= | Get From Dictionary | ${res} | pxe_engine |
        | Dictionary Should Contain Key | ${engine} | version |
        | Dictionary Should Contain Key | ${engine} | last_updated |
        | ${ver}= | Get From Dictionary | ${engine} | version |
        | ${upd}= | Get From Dictionary | ${engine} | last_updated |
        | Log | ${ver} |
        | Log | ${upd} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.encryptionstatus(**kwargs)
