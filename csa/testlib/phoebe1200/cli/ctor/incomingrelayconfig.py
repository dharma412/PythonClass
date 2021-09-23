#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/incomingrelayconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import clictorbase
from clictorbase import REQUIRED, DEFAULT, IafCliError, \
    IafCliParamMap, IafCliConfiguratorBase

from sal.deprecated.expect import EXACT


class incomingrelayconfig(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    def __call__(self):
        self._writeln('incomingrelayconfig')
        return self

    def setup(self, enable_relays=''):
        self._query_response('SETUP')
        self._query_response(enable_relays)
        self._to_the_top(self.newlines)

    def relaylist(self):
        self._query_response('RELAYLIST')
        return incomingrelayconfigRelaylist(self._get_sess())


class incomingrelayconfigRelaylist(clictorbase.IafCliConfiguratorBase):
    """incomingrelayconfig -> Relaylist"""

    class InvalidCharacterError(IafCliError):
        pass

    class InvalidHostError(IafCliError):
        pass

    class InvalidHeaderError(IafCliError):
        pass

    newlines = 2

    def __init__(self, sess):

        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('Invalid character', EXACT): self.InvalidCharacterError,
            ('Invalid incoming relay host entry', EXACT): self.InvalidHostError,
            ('custom header must be no', EXACT): self.InvalidHeaderError
        })

    def new(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['relay_name'] = \
            ['name for this incoming relay', REQUIRED]
        param_map['address'] = \
            ['address of the incoming relay.', REQUIRED]
        param_map['header_type'] = \
            ['use the "Received:" header or a custom ', DEFAULT, True]
        param_map['custom_header_name'] = \
            ['Enter the custom header name', REQUIRED]
        param_map['special_character'] = \
            ['enter the special character or string', DEFAULT]
        param_map['received_header_position'] = \
            ['position of the "Received:" header', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('NEW')
        return self._process_input(param_map)

    def edit(self, entry=''):

        self._query_response('EDIT')
        self._query_select_list_item(entry)
        return incomingrelayconfigRelaylistEdit(self._get_sess())

    def delete(self, entry=''):
        self._query_response('DELETE')
        self._query_select_list_item(entry)
        self._to_the_top(self.newlines)

    def print_table(self):
        self._query_response('PRINT')
        self._expect('\n')
        raw = self._read_until('Choose the operation ')
        self._to_the_top(self.newlines)
        return raw


class incomingrelayconfigRelaylistEdit(clictorbase.IafCliConfiguratorBase):
    """incomingrelayconfig -> Relaylist->Edit"""

    class InvalidCharacterError(IafCliError):
        pass

    class InvalidHostError(IafCliError):
        pass

    class InvalidHeaderError(IafCliError):
        pass

    newlines = 3

    def __init__(self, sess):

        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('Invalid character', EXACT): self.InvalidCharacterError,
            ('Invalid incoming relay host entry', EXACT): self.InvalidHostError,
            ('custom header must be no', EXACT): self.InvalidHeaderError
        })

    def name(self, relay_name=''):
        self._query_response('NAME')
        self._query_response(relay_name)
        self._to_the_top(self.newlines)

    def host(self, address=''):
        self._query_response('HOST')
        self._query_response(address)
        self._to_the_top(self.newlines)

    def type(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['header_type'] = \
            ['use the "Received:" header or a custom ', DEFAULT, True]
        param_map['custom_header_name'] = \
            ['Enter the custom header name', REQUIRED]
        param_map['special_character'] = \
            ['enter the special character or string', DEFAULT]
        param_map['received_header_position'] = \
            ['position of the "Received:" header', DEFAULT]
        param_map.update(input_dict or kwargs)

        self._query_response('TYPE')
        return self._process_input(param_map)

    def position(self, received_header_position=''):
        self._query_response('POSITION')
        self._query_response(received_header_position)
        self._to_the_top(self.newlines)

    def match(self, special_character=''):
        self._query_response('MATCH')
        self._query_response(special_character)
        self._to_the_top(self.newlines)

    def header(self, custom_header_name=''):
        self._query_response('HEADER')
        self._query_response(custom_header_name)
        self._to_the_top(self.newlines)
