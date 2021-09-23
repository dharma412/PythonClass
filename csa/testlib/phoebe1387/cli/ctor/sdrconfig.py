#!/usr/bin/env python

"""ESA Command Line Interface (CLI): sdrconfig
"""

import clictorbase

from clictorbase import DEFAULT
from sal.containers.yesnodefault import is_yes


class sdrconfig(clictorbase.IafCliConfiguratorBase):
    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)
        self._new_lines = 4

    def is_enabled(self):
        self.clearbuf()
        self._writeln('sdrconfig')
        index = self._query(
            'Would you like to disable the Sender Domain Reputation check',
            'Would you like to enable the Sender Domain Reputation check')
        if index == 0:
            self._to_the_top(self._new_lines)
            return True
        else:
            self._to_the_top(1)
            return False

    def enable(self, include_additional_attributes=DEFAULT, accept_end_user_license=DEFAULT,
               block_msg_based_on_srd_verdict=DEFAULT, sdr_verdict_upto_which_msg_should_be_blocked=DEFAULT):
        self.clearbuf()
        self._writeln('sdrconfig')
        index = self._query(
            'Would you like to disable the Sender Domain Reputation check',
            'Would you like to enable the Sender Domain Reputation check')
        if index == 0:
            self._info("Sender Domain Reputation check is already enabled")
            self._query_response(DEFAULT)
        else:
            self._query_response('Y')

        self._query('Do you want to include these additional attributes')
        self._query_response(include_additional_attributes)

        if is_yes(include_additional_attributes):
            self._query('I accept the Cisco Content Security Supplemental End User License Agreement')
            self._query_response(accept_end_user_license)

        self._query('Do you want to block messages based on Sender Domain Reputation verdict')
        self._query_response(block_msg_based_on_srd_verdict)
        if is_yes(block_msg_based_on_srd_verdict):        
            self._query('Choose the sender domain reputation verdict upto which email should')
            self._query_response(sdr_verdict_upto_which_msg_should_be_blocked)
        self._to_the_top(1)
        self._new_lines = 4

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
        self._new_lines = 2

    def edit(self, include_additional_attributes=DEFAULT, accept_end_user_license=DEFAULT,
             block_msg_based_on_srd_verdict=DEFAULT, sdr_verdict_upto_which_msg_should_be_blocked=DEFAULT):
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
            self._query_response(DEFAULT)

        self._query('Do you want to include these additional attributes')
        self._query_response(include_additional_attributes)

        if is_yes(include_additional_attributes):
            self._query(
                'I accept the Cisco Content Security Supplemental End User License Agreement')
            self._query_response(accept_end_user_license)

        self._query(
            'Do you want to block messages based on Sender Domain Reputation verdict')
        self._query_response(block_msg_based_on_srd_verdict)
        if is_yes(block_msg_based_on_srd_verdict):
            self._query(
                'Choose the sender domain reputation verdict upto which email should')
            self._query_response(sdr_verdict_upto_which_msg_should_be_blocked)
        self._to_the_top(1)
        self._new_lines = 4

    def batch(self, **kwargs):
        action = kwargs.get('action')
        share_extended_info = kwargs.get('share_extended_info')
        block_range = kwargs.get('block_range')
        verdict = kwargs.get('verdict')
        cmd = 'sdrconfig domainreputation'

        if action:
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

        if block_range:
            if block_range.lower() not in ['enable', 'disable']:
                raise ValueError('Invalid value {invalid_param} passed for'
                                 ' "share_extended_info" parameter. Allowed'
                                 ' values are: Enable or Disable'.
                                 format(invalid_param=block_range))
            else:
                cmd += ' block_range {action}'.format(
                    action=block_range.lower())

        if verdict:
            if verdict.lower() not in ['awful', 'poor', 'tainted', 'weak', 'unknown', 'neutral']:
                raise ValueError('Invalid arguments passed for sdrconfig'.
                                 format(invalid_param=verdict))
            else:
                cmd += ' {action}'.format(action=verdict.lower())

        self._info('BATCH COMMAND: %s' % cmd)
        self._to_the_top(1)
        self.clearbuf()
        self._writeln(cmd)
        self._wait_for_prompt()
        self._info(self.getbuf())

