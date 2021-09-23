#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/keywords/resume_listener.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $

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

