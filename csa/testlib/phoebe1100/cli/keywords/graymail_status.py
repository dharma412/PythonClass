#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/graymail_status.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

from common.cli.clicommon import CliKeywordBase
import traceback


class GraymailStatus(CliKeywordBase):
    """
    cli -> graymailstatus

    Provides keywords to get graymail engine status
    """

    def get_keyword_names(self):
        return ['graymail_status']

    def graymail_status(self):
        """
        Provides Graymail version and rule information.

        CLI -> graymailstatus

        *Returns*:
          Dictionary with following component as keys:
          - `graymail_library`
          - `graymail_tools`

          Each key is a dictionary having 'update_date' and 'version' as keys

        *Examples*:
        | ${Status}= | Graymail Status |
        | ${rules}= | Get From Dictionary | ${Status} | graymail_library |
        | ${rules_ver}= | Get From Dictionary | ${rules} | version |
        | ${rules_date}= | Get From Dictionary | ${rules} | update_date |
        """
        try:
            return dict(self._cli.graymailstatus().status())
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e
