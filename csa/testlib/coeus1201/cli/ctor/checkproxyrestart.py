#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/checkproxyrestart.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

import re
import time
from clictorbase import IafCliConfiguratorBase
from common.cli.cliexceptions import  CliError

class checkproxyrestart(IafCliConfiguratorBase):
    """checkproxyrestart - Checks if changes to the current config requires 
                           a proxy restart or not.
    """

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):

        self.clearbuf()
        self._writeln('checkproxyrestart')
        text = self._sess.read_until()

        no_change_text = re.compile\
                         ('no changes in current config', re.MULTILINE)
        restart_not_required_text = re.compile\
                         ('will not be required', re.MULTILINE)
        restart_after_commit_text = re.compile\
                         ('will restart after Commit', re.MULTILINE)
        
        print "Buffer (checkproxyrestart): %s" %text
        if text:
            if no_change_text.search(text):
                return 'NO_CHANGE'
            if restart_not_required_text.search(text):
                return 'RESTART_NOT_REQUIRED'
            if restart_after_commit_text.search(text):
                return 'RESTART_AFTER_COMMIT'
            else:
                raise CliError('checkproxyrestart() | CLIException | Unexpected command output: %s'%text) 
        else:
            raise CliError('checkproxyrestart() | CLIException | Empty Buffer.') 
