#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/sdrconfig.py#1 $
# $DateTime: 2020/01/06 01:25:43 $
# $Author: saurgup5 $

"""ESA Command Line Interface (CLI): sdrconfig
"""

import clictorbase

class sdrconfig(clictorbase.IafCliConfiguratorBase):
    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def is_enabled(self):
        self.clearbuf()
        self._writeln('sdrconfig')
        index = self._query(
            'Would you like to disable the Sender Domain Reputation check',
            'Would you like to enable the Sender Domain Reputation check')
        self._to_the_top(2)
        return True if index == 0 else False

    def enable(self, include_additional_attributes='Y'):
        self.clearbuf()
        self._writeln('sdrconfig')
        index = self._query(
            'Would you like to disable the Sender Domain Reputation check',
            'Would you like to enable the Sender Domain Reputation check')
        if index == 0:
            self._info("Sender Domain Reputation check is already enabled")
        else:
            self._query_response('Y')
            self._query_response(include_additional_attributes)
        self._to_the_top(1)

    def disable(self):
        self.clearbuf()
        self._writeln('sdrconfig')
        index = self._query(
            'Would you like to disable the Sender Domain Reputation check',
            'Would you like to enable the Sender Domain Reputation check')
        if index == 1:
            self._info("Sender Domain Reputation check is already disabled")
        else:
            self._query_response('Y')
        self._to_the_top(1)

    def edit(self, include_additional_attributes='N'):
        self.clearbuf()
        self._writeln('sdrconfig')
        index = self._query(
            'Would you like to disable the Sender Domain Reputation check',
            'Would you like to enable the Sender Domain Reputation check')
        if index == 1:
            self._warn("Sender Domain Reputation check is disabled")
            self._warn(
                "Enable Sender Domain Reputation check first to EDIT settings")
        else:
            self._query_response('')
            self._query_response(include_additional_attributes)
        self._to_the_top(1)

    def batch(self, **kwargs):
        action = kwargs.get('action')
        share_extended_info = kwargs.get('share_extended_info')
        cmd = 'sdrconfig domainreputation'

        if action is None:
            raise ValueError('"action" parameter cannot be None. '
                             'Please pass either Enable or Disable')
        else:
            if action.lower() not in ['enable', 'disable']:
                raise ValueError('Invalid value {invalid_param} passed for'
                                 ' "action" parameter. Allowed'
                                 ' values are: Enable or Disable'.
                                 format(invalid_param=action))
            else:
                cmd += ' {action}'.format(action=action.lower())

        if share_extended_info:
            if share_extended_info.lower() not in ['enable', 'disable']:
                raise ValueError('Invalid value {invalid_param} passed for'
                                 ' "share_extended_info" parameter. Allowed'
                                 ' values are: Enable or Disable'.
                                 format(invalid_param=share_extended_info))
            else:
                cmd += ' share_extended_info {action}'.format(
                    action=share_extended_info.lower())

        self._info('BATCH COMMAND: %s' % cmd)
        self._to_the_top(1)
        self.clearbuf()
        self._writeln(cmd)
        self._wait_for_prompt()
        self._info(self.getbuf())
