#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/keywords/resume_listener.py#1 $ $DateTime: 2020/06/10 22:29:20 $ $Author: sarukakk $

from common.cli.clicommon import CliKeywordBase

class ResumeListener(CliKeywordBase):

    """Keywords for resumelistener CLI command."""

    def get_keyword_names(self):
        return ['resumelistener',]

    def resumelistener(self):
        """Resume listener.

        Exceptions:
        - `ConfigError`: in case listener can not be resumed.

        Examples:
        | Resume Listener |
        """
        self._cli.resumelistener()

