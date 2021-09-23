#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/supportrequest_status.py#1 $
# $DateTime: 2019/06/27 23:26:24 $
# $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class SupportrequestStatus(CliKeywordBase):
    """
    Fetch Support Request status.
    CLI command: supportrequeststatus
    """

    def get_keyword_names(self):
        return ['supportrequest_status', ]

    def supportrequest_status(self, *args):
        """
        CLI command: supportrequeststatus

        *Parameters:*
        - `as_dictionary`: Return result formatted as dictionary. YES or NO.

        *Return:*
        Dictionary or raw output.
        Dictionary has the following keys which are dictionaries themselves:
        - _support_request_

        Which has keys:
        - _version_
        - _last_updated_

        _Example_:\n
        {'support_request': {'version': '1.0',
                        'last_updated': '19 Jul 2012 00:18 (GMT +00:00)\r'}}

        *Examples:*
        | Supportrequest Status | as_dictionary=y |
        | Supportrequest Status | as_dictionary=n |

        | ${result}= | Supportrequest Status |
        | ${support_request}= | Get From Dictionary | ${result} | support_request |
        | Dictionary Should Contain Key | ${support_request} | version |
        | Dictionary Should Contain Key | ${support_request} | last_updated |
        | ${version}= | Get From Dictionary | ${support_request} | version |
        | ${last_updated}= | Get From Dictionary | ${support_request} | last_updated |
        | Log | ${version} |
        | Log | ${last_updated} |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.supportrequeststatus(**kwargs)
