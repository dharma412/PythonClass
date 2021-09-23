#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/keywords/outbreak_flush.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

"""
SARF CLI command: outbreakflush
"""

from common.cli.clicommon import CliKeywordBase


class OutbreakFlush(CliKeywordBase):
    """
    Flush the Outbreak Filters rules.

    CLI command: outbreakflush
    """

    def get_keyword_names(self):
        return ['outbreak_flush', ]

    def outbreak_flush(self, *args):
        """Flush the Outbreak Filters rules.

        CLI command: outbreakflush

        *Parameters:*
        - `confirm`: Confirm flushing the rules. YES or NO.

        *Return:*
        True(Boolean) if cleared successfully.
        Else raise an exception.

        *Exceptions:*
        - `NoOutbreakFeatureKeyError`: No feature key.
        - `OutbreakIsNotEnabledError`: The feature is disabled.
        - `FlushingRulesFailedError`: Failed to flush the rules.

        *Examples:*
        | Outbreak Flush | confirm=yes |
        """
        kwargs = self._convert_to_dict(args)
        return self._cli.outbreakflush(**kwargs)
