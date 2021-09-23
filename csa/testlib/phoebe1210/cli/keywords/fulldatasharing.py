#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/keywords/fulldatasharing.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

from common.cli.clicommon import CliKeywordBase


class FullDatasharing(CliKeywordBase):
    """
    Share unhashed filenames with SenderBase Information Service.
    CLI command: fulldatasharing
    """

    def get_keyword_names(self):
        return ['fulldatasharing_setup', ]

    def fulldatasharing_setup(self, *args):
        """Share unhashed filenames with SenderBase Information Service.

        CLI command: fulldatasharing > setup

        *Parameters:*
        - `enable`: Share unhashed filenames with SenderBase Information Service. YES or NO.

        *Return:*
        None

        *Examples:*
        | Fulldatasharing Setup | enable=yes |
        | Fulldatasharing Setup | enable=no |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.fulldatasharing().setup(**kwargs)
