#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/altsrchost.py#1 $

"""
IAF 2 CLI command: altsrchost
"""

import clictorbase as ccb
from sal.deprecated.expect import EXACT

REQUIRED = ccb.REQUIRED
DEFAULT = ccb.DEFAULT

DEBUG = True


class altsrchost(ccb.IafCliConfiguratorBase):
    class MaximumEntriesImportError(ccb.IafCliError): pass

    class AltsrchostAddressError(ccb.IafCliError): pass

    class MaximumEntriesError(ccb.IafCliError): pass

    class EntryExistenceError(ccb.IafCliError): pass

    class ExportEntriesError(ccb.IafCliError): pass

    class MachineReachError(ccb.IafCliError): pass

    class InputOutputError(ccb.IafCliError): pass

    class InterfaceError(ccb.IafCliError): pass

    class MatchKeyError(ccb.IafCliError): pass

    class EntryError(ccb.IafCliError): pass

    def __init__(self, sess):
        ccb.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('remove one before trying to add a new entry',
             EXACT): self.MaximumEntriesError,
            ('An altsrchost address may be one of the following',
             EXACT): self.AltsrchostAddressError,
            ('There are no entries in the source delivery table',
             EXACT): self.EntryExistenceError,
            ('Export failed', EXACT): self.ExportEntriesError,
            ('Exceeded maximum entry count',
             EXACT): self.MaximumEntriesImportError,
            ('Invalid match key', EXACT): self.MatchKeyError,
            ('Unknown interface', EXACT): self.InterfaceError,
            ('Invalid entry', EXACT): self.EntryError,
            ('Unable to perform operation due to an I/O error',
             EXACT): self.InputOutputError,
            ('Could not reach target machine', EXACT): self.MachineReachError
        })

    def __call__(self):
        self._writeln('altsrchost')
        return self

    def new(self, address=REQUIRED, interface=DEFAULT):
        self.level = 1
        self._query_response('NEW')
        self._query_response(address)
        self._query_select_list_item(interface)
        self._to_the_top(self.level)

    def edit(self, address_to_edit=REQUIRED, address=DEFAULT,
             interface=DEFAULT):
        self.level = 1
        self._query_response('EDIT')
        self._query_response(address_to_edit)
        self._query_response(address)
        self._query_select_list_item(interface)
        self._to_the_top(self.level)

    def print_mappings(self):
        self.level = 1
        self._query_response('PRINT')
        self._expect('\n')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.level)
        return raw

    def clear(self):
        self.level = 1
        self._query_response('CLEAR')
        self._to_the_top(self.level)

    def import_mappings(self, import_file=REQUIRED):
        self.level = 1
        self._query_response('IMPORT')
        self._query_response(import_file)
        self._to_the_top(self.level)

    def export_mappings(self, export_file=REQUIRED):
        self.level = 1
        self._query_response('EXPORT')
        self._query_response(export_file)
        self._to_the_top(self.level)

    def delete(self, address=REQUIRED, confirmation=DEFAULT):
        self.level = 1
        self._query_response('DELETE')
        self._query_response(address)
        self._query_response(confirmation)
        self._to_the_top(self.level)


if __name__ == '__main__':
    from iafframework import iafcfg

    my_host = iafcfg.get_hostname()
    iface = 'Management'
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
        iface = 'main'
    except NameError:
        cli_sess = ccb.get_sess()
        if my_host.find('.eng') > -1:
            iface = 'main'
    ash = altsrchost(cli_sess)

    ash().new(address='address@', interface=iface)
    print ash().print_mappings()
    ash().edit(address_to_edit='address@', address='addressnew@',
               interface=iface)
    print ash().print_mappings()
    ash().export_mappings(export_file='file')
    ash().delete(address='addressnew@')
    ash().import_mappings(import_file='file')
    print ash().print_mappings()
    ash().clear()
