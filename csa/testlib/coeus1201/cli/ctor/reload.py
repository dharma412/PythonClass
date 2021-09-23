#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/reload.py#1 $
# $DateTime: 2019/08/14 09:58:47 $
# $Author: uvelayut $

"""
SARF CLI command: reload
"""

import clictorbase

class reload(clictorbase.IafCliConfiguratorBase):
    """
    Resets the DUT to default state
    """
    def __call__(self, confirm_action='y'):

        command = 'reload'

        #Issue the CLI command in SSH
        self._info('Issuing RELOAD command')
        self._writeln(command)

        #Confirm the action of reload
        idx = self._query('Are you sure you want to continue? [y|n] ')
        if idx == 0 and confirm_action == 'y':
            self._writeln(confirm_action)
        elif confirm_action == 'n':  #If typed 'n' then return and do nothing
            self._writeln(confirm_action)
            return
        else:
            raise ConfigError, "reload: unexpected response"

        #Handle the confirmation for 2nd time
        self._info('Confirming RELOAD command action')
        idx = self._query('Are you *really* sure you want to continue? If so, type \'YES\': ')

        #Issue 'YES' to confirm the reload command and return as the DUT reboots in this case
        if idx == 0:
            self._writeln('YES')
        #Handle the Question
            self._info('Do you want this data to be erased securely? [N]> ')
            idx = self._query('Do you want this data to be erased securely? [N]>')
            if idx == 0:
                self._writeln('N')
                return
            else:
                raise ConfigError, "reload: Unexpected response CLI Buffer. Question 'Do you want this data to be erased securely?' did not appear." 
        else:
            raise ConfigError, "reload: Unexpected CLI Buffer. Question 'Are you *really* sure you want to continue?' did not appear." 


