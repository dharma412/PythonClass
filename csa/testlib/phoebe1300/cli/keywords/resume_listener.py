#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/keywords/resume_listener.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase
import traceback


class ResumeListener(CliKeywordBase):
    """Keywords for resumelistener CLI command."""

    def get_keyword_names(self):
        return ['resume_listener', ]

    def resume_listener(self, listener_name='All'):
        """Resume listener.

        Parameters:
        - `listener_name` : name of the listener like All,private_qmqp etc..

        Examples:
        | Resume Listener | listener_name=private_qmap |
        """
        try:
            self._cli.resumelistener(listener_name)
        except Exception, e:
            self._cli.restart()
            traceback.print_exc()
            raise e
