#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/alertconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

"""
IAF 2 CLI command: alertconfig
"""

import string
from sal.exceptions import ConfigError
import clictorbase
from clictorbase import REQUIRED, DEFAULT, IafCliError, \
    IafCliParamMap, IafCliConfiguratorBase
from sal.containers.yesnodefault import YES, NO
from sal.containers.yesnodefault import is_yes
from sal.deprecated.expect import EXACT

DEBUG = True


class SeveritiesSelectionError(IafCliError):
    pass


class DebounceIntervalError(IafCliError):
    pass


class alertconfig(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('You cannot pick', EXACT): SeveritiesSelectionError,
            ('debounce interval cannot be less',
             EXACT): DebounceIntervalError,
        })

    def __call__(self):
        self._writeln('alertconfig')
        return self

    def new(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(end_of_command='Choose the operation')
        param_map['address'] = ['email address', REQUIRED]
        param_map['alert_classes'] = ['Alert Classes', DEFAULT]
        param_map['severity_levels'] = ['Severity Level', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('NEW')
        return self._process_input(param_map)

    def print_alerts(self):
        """
            There is NO menu item PRINT in alertconfig menu.
            This is auxiliary operation to get information
            about configured alerts.

            Returns a raw output if any alert is configured on None.
            ##TODO:LOW implement raw parsing and structured result generation.
        """
        raw = ''
        try:
            raw = self._read_until(self._sub_prompt_user_match)
            if raw.find('Sending alerts to:') <= 0:
                raw = ''
        finally:
            # return to the CLI prompt
            self._writeln()  # not self._to_the_top(self.level) since
            # _query() has timeout read after
            # _read_until() call
            self._wait_for_prompt()  # to be sure of CLI state
        return raw

    def edit(self, address=REQUIRED, alert_class=REQUIRED, enable=DEFAULT,
             disable=DEFAULT, severity_levels=DEFAULT, **kwargs):

        self.newlines = 2
        self._query_response('EDIT')
        self._query_response(address)
        self._query_response(alert_class)
        if int(alert_class) == 9:
            idx = self._query('enable "Release and Support Notification?"', \
                              'disable "Release and Support Notification?"')
            if idx == 0:
                if enable == 'yes' or disable == 'no':
                    self._writeln('yes')
                elif enable == 'no' or disable == 'yes':
                    self._writeln('no')
            elif idx == 1:
                if disable == 'yes' or enable == 'no':
                    self._writeln('yes')
                elif disable == 'no' or enable == 'yes':
                    self._writeln('no')
        else:
            self._query_response(severity_levels)
        self._to_the_top(self.newlines)

    def delete(self, address=REQUIRED):
        self.newlines = 1
        self._query_response('DELETE')
        self._query_response(address)
        self._to_the_top(self.newlines)

    def clear(self):
        """
        returns 0 if cleared some alerts
        returns -1 if was no one alert configured (nothing to clear).
        """
        result = -1
        self.newlines = 1
        # check if menu CLEAR is available
        buf = self._read_until(self._sub_prompt_user_match)
        clearavailable = buf.find('CLEAR')
        if clearavailable > 0:
            # write directly since _query_response() has timeout read after
            # _read_until() call
            self._writeln('CLEAR')
            self._to_the_top(self.newlines)
            result = 0
        else:
            result = -1
            # return to the CLI prompt
            self._writeln()  # not self._to_the_top(self.level) since
            # _query() has timeout read after
            # _read_until() call

            self._wait_for_prompt()  # to be sure of CLI state
        return result

    def setup(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['initial_debounce_interval'] = \
            ['Initial number of seconds', DEFAULT]
        param_map['max_debounce_interval'] = \
            ['Maximum number of seconds', DEFAULT]
        param_map['auto_support'] = \
            ['enable Cisco IronPort AutoSupport', DEFAULT]
        param_map['reports'] = \
            ['weekly AutoSupport reports', DEFAULT]
        param_map['max_alerts'] = \
            ['Maximum number of alerts to save', DEFAULT]
        param_map['interface'] = \
            ['Choose the default interface to be used to deliver alerts', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('SETUP')
        return self._process_input(param_map)

    def from_address(self, dict_number=REQUIRED):
        self._query_response('FROM')
        return alertconfigFrom(self._get_sess())


class alertconfigFrom(IafCliConfiguratorBase):
    """alertconfig -> From"""

    def edit(self, address=REQUIRED):
        self.newlines = 1
        self._query_response('EDIT')
        self._query_response(address)
        self._to_the_top(self.newlines)

    def default(self):
        self.newlines = 1
        self._query_response('DEFAULT')
        self._to_the_top(self.newlines)


if __name__ == '__main__':
    def check_clear(res):
        """
        auxiliary function for alertconfig().clear() testing.
        """
        if res == 0:
            print 'Cleared some alerts. - OK'
        elif res == -1:
            print 'Nothing to clear!'
        else:
            print 'ERROR! UNEXPECTED RESULT CODE! SHOULD NEVER REACH THIS! '


    def check_print_alerts(expect_nothing_to_print=True):
        """
        auxiliary function for alertconfig().print_alerts() testing.
        """
        alerts = ac().print_alerts()
        if ('' == alerts and expect_nothing_to_print) or \
                ('' != alerts and not expect_nothing_to_print):
            res = 0
        else:
            res = -1
        print 'print_alerts:[%s]' % alerts
        assert 0 == res


    sess = clictorbase.get_sess()
    ac = alertconfig(sess)
    check_clear(ac().clear())
    check_clear(ac().clear())  # test if nothing to clear
    check_print_alerts()

    ac().new(address='mail@any.ua')
    ac().new(address='mail@any1.ua', alert_classes='2,3,4,5,6,7',
             severity_level='1')
    check_clear(ac().clear())
    check_print_alerts()

    ac().new(address='mail@any.ua')
    ac().new(address='mail@any1.ua', alert_classes='1', severity_level='2')
    ac().new(address='mail@any3.ua', alert_classes='1', severity_level='3')
    ac().new(address='mail@any4.ua', alert_classes='1', severity_level='4')
    ac().new(address='mail@any5.ua', alert_classes='1',
             severity_level='1,2,3,4')
    ac().new(address='mail@any6.ua', alert_classes='1,2,3,4,5,6,7',
             severity_level='1,2,3,4')
    ac().new(address='mail@any7.ua', alert_classes='2,3,4,5',
             severity_level='3')
    check_print_alerts(False)

    ac().edit(address='2', alert_classes='1', severity_level='2')
    ac().edit(address='3', alert_classes='5', severity_level='3')
    ac().edit(address='1', alert_classes='7', severity_level='5')
    ac().edit(address='5', alert_classes='1', severity_level='1')
    ac().edit(address='4', alert_classes='3', severity_level='1')
    check_print_alerts(False)

    ac().setup(initial_debounce_interval='25', max_debounce_interval='29',
               auto_support='n')
    ac().setup(initial_debounce_interval='25', max_debounce_interval='29',
               auto_support='y')
    ac().setup(initial_debounce_interval='0', auto_support='y', reports='n')
    ac().from_address().edit(address='safr@mail.com')
    ac().from_address().default()
    check_print_alerts(False)
    ac().delete(address='4')
    ac().delete(address='mail@any.ua')
    check_print_alerts(False)
    check_clear(ac().clear())
    check_print_alerts()
