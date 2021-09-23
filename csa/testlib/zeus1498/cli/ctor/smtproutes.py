#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/smtproutes.py#1 $ $DateTime: 2020/05/25 00:19:30 $ $Author: sarukakk $

"""
Command Line Interface (CLI)

command:
    - smtproutes
"""

from clictorbase import IafCliConfiguratorBase, IafCliValueError, DEFAULT, \
                       REQUIRED, IafCliParamMap, IafCliCtorNotImplementedError
from sal.deprecated.expect import REGEX, EXACT
from sal.containers.yesnodefault import YES


class smtproutes(IafCliConfiguratorBase):

    """smtproutes
    """

    newlines = 1

    def __init__(self,sess):
        IafCliConfiguratorBase.__init__(self, sess)
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
        self._writeln('smtproutes')
        return self

    def new(self, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command = 'Choose the operation')
        param_map['domain']         = ['Enter the domain', REQUIRED]
        param_map['dest_hosts']     = ['Enter the destination hosts', REQUIRED]
        param_map.update(input_dict or kwargs)
        self._query_response('NEW')
        self._process_input(param_map)

    def edit(self, hostname):
        global smtproutesEdit
        self._query_response('EDIT')
        self._query_response(hostname)
        return smtproutesEdit(self._get_sess())

    def delete(self, hostname):
        self._query_response('DELETE')
        self._query_response(hostname)
        # confirmation to clear.
        # Are you sure you want to reset the default route?
        self._query_response(YES)
        self._to_the_top(self.newlines)

    def print_all(self):
        self._query_response('PRINT')
        raw = self._read_until('Choose the operation')
        self._restart()
        return raw

    def export(self, filename):
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

class smtproutesEdit(IafCliConfiguratorBase):
    """smtproutes -> EDIT """

    newlines = 2

    def add(self, dest_hosts):
        self._query_response('ADD')
        self._query_response(dest_hosts)
        self._to_the_top(self.newlines)

    def remove(self, dest_hosts):
        self._query_response('REMOVE')
        self._query_response(dest_hosts)
        self._to_the_top(self.newlines)

    def replace(self, dest_hosts):
        self._query_response('REPLACE')
        self._query_response(dest_hosts)
        self._to_the_top(self.newlines)


if __name__=="__main__":
    from clictorbase import get_sess
    sess=get_sess()
    cli = smtproutes(sess)
    # testing new:
    cli().new(domain='1.1.1.1', dest_hosts='2.2.2.2')
    cli().new(domain='3.3.3.3', dest_hosts='2.2.2.2')
    cli().new(domain='5.5.5.5', dest_hosts='2.2.2.2', smtp_profiling='y', smtp_profile='test')
    cli().new(domain='4.4.4.4', dest_hosts='2.2.2.2', smtp_profiling='n')
    cli().new(domain='2.2.2.2', dest_hosts='2.2.2.2')

    # testing delete:
    cli().delete('1.1.1.1')
    cli().delete('2.2.2.2')
    # testing print_all:
    cli().print_all()
    # testing clear:
    cli().clear()
