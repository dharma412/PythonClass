#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/smtproutes.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

"""
SARF CLI command: smtproutes
"""

import clictorbase
from clictorbase import IafCliValueError, DEFAULT, REQUIRED, \
    IafCliParamMap, IafCliConfiguratorBase, \
    IafCliCtorNotImplementedError

from sal.containers.yesnodefault import YES
from sal.deprecated.expect import REGEX, EXACT


class smtproutes(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            # new error messages
            ('There is a maximum of \S+ routes.', REGEX): IafCliValueError,
            ('The value \S+ is already in the routing table.', REGEX): \
                IafCliValueError,
            ('There is already a default route set.', EXACT): \
                IafCliValueError,
            ('Routes may not contain more than \S+ destinations.', REGEX): \
                IafCliValueError,
            ('The host \S+ already has an alternate port (\d+).', REGEX): \
                IafCliValueError,
            ('The host \S+ is already using the standard port.', REGEX): \
                IafCliValueError,
            # delete error messages
            ('entry does not appear to be in the routing table', EXACT): \
                IafCliValueError,
            # import/export error messages
            ('Error reading file.', EXACT): IafCliValueError,
            ('Could not reach target machine:', EXACT): IafCliValueError,
            ('Valid characters are', EXACT): IafCliValueError,
            ('Import failed.', EXACT): IafCliValueError,
            ('Could not reach target machine:', EXACT): IafCliValueError,
            ('Unable to perform operation due to an I/O error.', EXACT): \
                IafCliValueError,
            ('Configuration filesystem is full.', EXACT): IafCliValueError,
            ('Error writing file.', EXACT): IafCliValueError,
        })

    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def new(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['domain'] = ['Enter the domain for which', REQUIRED]
        param_map['dest_hosts'] = ['Enter the destination hosts', REQUIRED]
        param_map['smtp_profiling'] = ['Do you want to associate an SMTP' \
                                       ' authentication profile', DEFAULT]
        # smtp_profiles is the configured profile name with 'smtpauthconfig'
        param_map['smtp_profile'] = ['Select the SMTP authentication' \
                                     ' profile to use:', REQUIRED, 1]
        param_map.update(input_dict or kwargs)
        self._query_response('NEW')
        self._process_input(param_map)

    def delete(self, domain, confirm=YES):
        self._query_response('DELETE')
        self._query_response(domain)
        # confirmation to clear.
        # Are you sure you want to reset the default route?
        self._query_response(confirm)
        self._to_the_top(self.newlines)

    def edit(self, domain, new_domain=DEFAULT):
        self._query_response('EDIT')
        self._query_response(domain)
        self._query_response(new_domain)
        return smtproutesEdit(self._get_sess())

    def print_all(self):
        self._query_response('PRINT')
        raw = self._read_until('Choose the operation')
        self._restart()
        return raw

    def export_routes(self, filename):
        self._query_response('EXPORT')
        self._query_response(filename)
        self._to_the_top(self.newlines)

    def import_routes(self, filename):
        self._query_response('IMPORT')
        self._query_response(filename)
        self._to_the_top(self.newlines)

    def clear(self):
        self._query_response('CLEAR')
        # confirmation  to clear.
        # Are you sure you want to delete all of the configured routes?
        self._query_response(YES)
        self._to_the_top(self.newlines)

    def clusterset(self):
        raise IafCliCtorNotImplementedError

    def clustershow(self):
        raise IafCliCtorNotImplementedError


class smtproutesEdit(clictorbase.IafCliConfiguratorBase):
    newlines = 1
    clictorbase.set_ignore_unanswered_questions(ignore=True)

    def add(self, input_dict=None, **kwargs):
        """Add new destination hosts"""
        self._query_response('ADD')
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['dest_hosts'] \
            = ['the additional destination hosts, separated by commas', REQUIRED]
        param_map['smtp_profiling'] = ['Do you want to associate an SMTP' \
                                       ' authentication profile', DEFAULT]
        param_map['smtp_profiling_another'] = \
            ['associate another SMTP authentication', DEFAULT]
        param_map['smtp_profiling_disassociate'] = \
            ['to disassociate the SMTP authentication profile', DEFAULT]
        # smtp_profiles is the configured profile name with 'smtpauthconfig'
        param_map['smtp_profile'] = ['Select the SMTP authentication' \
                                     ' profile to use:', REQUIRED, 1]
        param_map.update(input_dict or kwargs)
        self._process_input(param_map)

    def replace(self, input_dict=None, **kwargs):
        """Specify a new destination or set of destinations"""
        self._query_response('REPLACE')
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['dest_hosts'] \
            = ['the destination hosts, separated by commas', REQUIRED]
        param_map['smtp_profiling'] = ['Do you want to associate an SMTP' \
                                       ' authentication profile', DEFAULT]
        param_map['smtp_profiling_another'] = \
            ['associate another SMTP authentication', DEFAULT]
        param_map['smtp_profiling_disassociate'] = \
            ['to disassociate the SMTP authentication profile', DEFAULT]
        # smtp_profiles is the configured profile name with 'smtpauthconfig'
        param_map['smtp_profile'] = ['Select the SMTP authentication' \
                                     ' profile to use:', REQUIRED, 1]
        param_map.update(input_dict or kwargs)
        self._process_input(param_map)

    def remove(self, input_dict=None, **kwargs):
        """Remove an existing destination"""
        self._query_response('REMOVE')
        param_map = IafCliParamMap(end_of_command='Choose the operation')
        param_map['dest_hosts'] \
            = ['the destination you would like to remove', REQUIRED]
        param_map['smtp_profiling'] = ['Do you want to associate an SMTP' \
                                       ' authentication profile', DEFAULT]
        param_map['smtp_profiling_another'] = \
            ['associate another SMTP authentication', DEFAULT]
        param_map['smtp_profiling_disassociate'] = \
            ['to disassociate the SMTP authentication profile', DEFAULT]
        # smtp_profiles is the configured profile name with 'smtpauthconfig'
        param_map['smtp_profile'] = ['Select the SMTP authentication' \
                                     ' profile to use:', REQUIRED, 1]
        param_map.update(input_dict or kwargs)
        self._process_input(param_map)
