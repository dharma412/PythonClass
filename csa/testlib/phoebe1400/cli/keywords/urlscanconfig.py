#!/usr/bin/env python

from common.cli.clicommon import CliKeywordBase


class UrlScanConfig(CliKeywordBase):
    """ cli -> urlscanconfig """
    def get_keyword_names(self):
        return ['urlscanconfig']

    def urlscanconfig(self, *args):
        """Enables or disables default url scanning in attachments.

        *Parameters:*
        - `enable_attachment_scanning`: Provide Yes or No

        *Examples:*
        | Urlscanconfig | enable_attachment_scanning=Yes |
        | Urlscanconfig | enable_attachment_scanning=No  |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.urlscanconfig(kwargs)
