#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/dmarcconfig.py#1 $ $DateTime: 2019/06/27 23:26:24 $ $Author: aminath $

"""
SARF CLI command: dmarcconfig
"""

import clictorbase
from clictorbase import DEFAULT, REQUIRED
from sal.containers.yesnodefault import YES, NO, is_yes


class dmarcconfig(clictorbase.IafCliConfiguratorBase):
    level = 1

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def setup(self, input_dict=None, **kwargs):
        add_header = kwargs.pop('add_header', None)
        remove_header_number = kwargs.pop('remove_header', None)

        param_map = clictorbase.IafCliParamMap(
            end_of_command='Choose the operation')
        param_map['modify_dmarc_report'] = ['modify DMARC report settings',
                                            DEFAULT]
        param_map['time_report'] = ['time of day to generate', DEFAULT]
        param_map['send_report'] = ['send DMARC error reports', DEFAULT]
        param_map['entity_name'] = ['entity name responsible', DEFAULT]
        param_map['additional_contact'] = ['additional contact information to ' \
                                           'be added', DEFAULT]
        param_map['send_copy'] = ['send a copy of all aggregate reports', \
                                  DEFAULT]
        param_map['email_addresses'] = ['list of email addresses', DEFAULT]
        param_map['bypass_addresslist'] = ['bypass DMARC verification for an ' \
                                           'addresslist', DEFAULT]
        param_map['address_list'] = ['Select the address list', DEFAULT]
        param_map['bypass_header'] = ['specific header fields', DEFAULT]

        param_map.update(input_dict or kwargs)
        self._query_response('SETUP')

        if is_yes(kwargs.get('bypass_header')):
            self._process_input(param_map, do_restart=False)
            if add_header:
                dmarcconfigbypassheader(self._get_sess()).add(add_header)
            if remove_header_number:
                dmarcconfigbypassheader(self._get_sess()) \
                    .remove(remove_header_number)
        else:
            self._process_input(param_map)

    def profiles(self):
        self._query_response('PROFILES')
        return dmarcconfigprofiles(self._get_sess())


class dmarcconfigbypassheader(clictorbase.IafCliConfiguratorBase):
    newlines = 2

    def add(self, header):
        self._writeln('ADD')
        self._writeln(header)
        self._to_the_top(self.newlines)

    def remove(self, headernumber):
        self._writeln('REMOVE')
        self._writeln(headernumber)
        self._to_the_top(self.newlines)


class dmarcconfigprofiles(clictorbase.IafCliConfiguratorBase):
    newlines = 2
    COMMON_PARAMS = \
        {'reject_action': ['DMARC policy is reject', DEFAULT],
         'select_quarantine_reject': ['when the policy action is ' \
                                      'reject', DEFAULT],
         'smtp_response_code': ['SMTP response code', DEFAULT],
         'smtp_response_text': ['SMTP response text', DEFAULT],
         'quarantine_action': ['DMARC policy is quarantine', DEFAULT],
         'select_quarantine': ['when the policy action is ' \
                               'quarantine', DEFAULT],
         'smtp_action_temporary': ['temporary failure', DEFAULT],
         'smtp_code_temporary': ['code for rejected messages in ' \
                                 'case of temporary failure', DEFAULT],
         'smtp_text_temporary': ['text for rejected messages in ' \
                                 'case of temporary failure', DEFAULT],
         'smtp_action_permanent': ['permanent failure', DEFAULT],
         'smtp_code_permanent': ['code for rejected messages in ' \
                                 'case of permanent failure', DEFAULT],
         'smtp_text_permanent': ['text for rejected messages in ' \
                                 'case of permanent failure', DEFAULT]
         }

    def new(self, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(
            end_of_command='Choose the operation')
        param_map['name'] = ['name of the new DMARC', REQUIRED]
        for k, v in self.COMMON_PARAMS.iteritems():
            param_map[k] = v
        param_map.update(input_dict or kwargs)
        self._query_response('NEW')
        return self._process_input(param_map)

    def edit(self, profile_name, input_dict=None, **kwargs):
        param_map = clictorbase.IafCliParamMap(
            end_of_command='Choose the operation')
        param_map['name'] = ['name of DMARC verification profile', DEFAULT]
        for k, v in self.COMMON_PARAMS.iteritems():
            param_map[k] = v
        param_map.update(input_dict or kwargs)
        self._query_response('EDIT')
        self._query_select_list_item(profile_name)
        return self._process_input(param_map)

    def delete(self, profile_name):
        self._query_response('DELETE')
        self._query_select_list_item(profile_name)
        self._to_the_top(self.newlines)

    def Print(self, profile_name):
        self._query_response('PRINT')
        self._query_select_list_item(profile_name)
        self._expect('\n')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.newlines)
        return raw

    def Import(self, file_name):
        self._query_response('IMPORT')
        self._query_response(file_name)
        self._to_the_top(self.newlines)

    def export(self, file_name):
        self._query_response('EXPORT')
        self._query_response(file_name)
        self._to_the_top(self.newlines)

    def clear(self, confirm=DEFAULT):
        self._query_response('CLEAR')
        self._query_response(confirm)
        self._to_the_top(self.newlines)
