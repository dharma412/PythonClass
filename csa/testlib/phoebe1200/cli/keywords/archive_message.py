#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/archive_message.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase
import traceback


class ArchiveMessage(CliKeywordBase):
    """
    cli -> archivemessage

    Provides keyword to archive message
    """

    def get_keyword_names(self):
        return ['archive_message',
                ]

    def archive_message(self, mid):
        """
        Archive the message for the given mid into an mbox file in the
        configuration directory.

        *Parameters*:
        - `mid`: MID of the message to be archived

        *Returns*:
          Output of the archive message command

        *Examples*:
        | ${Status}= | Archive Message | 1 |
        """
        try:
            return self._cli.archivemessage(mid)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e
