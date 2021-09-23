#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/keywords/status.py#1 $

from common.cli.clicommon import CliKeywordBase
import common.cli.cliexceptions as cliexceptions

class Status(CliKeywordBase):
    """Displays the system status.

    If the 'detail' option is set to 'yes', result will contain additional
    information.
    """

    def get_keyword_names(self):
        return [
            'status',
        ]

    def status(self, detail='yes'):
        """Status.

        Use this keyword to get current system status.

        Parameters:
        - `detail`: displaying additional information option. Either \'yes\' or
        \'no\'. Default value is \'yes\'.

        Examples:
        | Status |

        | Status | detail=yes |
        """

        detail_options = {'yes': True, 'no': False}
        detail = detail.lower()
        if detail not in detail_options.keys():
            raise cliexceptions.CliValueError(
                'Detail option should be either \'yes\' or \'no\'.')
        return self._cli.status(detail_options[detail])
