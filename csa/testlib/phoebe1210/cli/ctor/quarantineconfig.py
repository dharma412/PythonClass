#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/quarantineconfig.py#1 $
# $DateTime: 2019/05/07 03:16:10 $
# $Author: bimmanue $

"""
SARF CLI command: quarantineconfig
"""

import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliParamMap, \
    DEFAULT, REQUIRED, IafCliValueError

from sal.deprecated.expect import REGEX, EXACT
from sal.containers.yesnodefault import YES, NO, is_yes, is_no
import re
from sal.containers.cfgholder import CfgHolder


class quarantineconfig(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    def __init__(self, sess):

        try:
            IafCliConfiguratorBase.__init__(self, sess)

        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('retention period must be', EXACT): IafCliValueError,
            ('There are no messages', EXACT): IafCliValueError,
            ('cannot be deleted.', EXACT): IafCliValueError,
            ('Please answer Yes or No', EXACT): IafCliValueError,
            ('Current quarantine allocation is over the system maximum', \
             EXACT): IafCliValueError,
            ('Insufficient space to create a new quarantine.', EXACT): \
                IafCliValueError,
            ('Only \d+ MB is available for quarantine allocation.', REGEX): \
                IafCliValueError,
            ('There is not enough space to resize the quarantine', EXACT): \
                IafCliValueError,
            ('Could not access the \S+ quarantine', REGEX): IafCliValueError,
            ('You do not have access to any quarantine.', EXACT): \
                IafCliValueError,
            # Builtin quarantine "%s" cannot be deleted
            ('cannot be deleted.', EXACT): IafCliValueError,
            ('Quarantine database error', EXACT): IafCliValueError,
            ('No users in the Operators/Guests groups have access to', EXACT): \
                IafCliValueError,
            ('All users have access to this quarantine', EXACT):
                IafCliValueError,
        })

    def __call__(self, batch_cmd=''):

        if batch_cmd:
            self._writeln('quarantineconfig %s' % batch_cmd)

            if batch_cmd.lower() == 'resetdb':
                self._query_response(YES)

            return self._read_until()

        self._writeln(self.__class__.__name__)
        return self

    def new(self, input_dict=None, **kwargs):
        _add_roles = kwargs.pop('add_roles', None)
        _del_roles = kwargs.pop('delete_roles', None)
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['name'] = ['enter the name for', REQUIRED]
        param_map['period'] = ['period for this quarantine', \
                               REQUIRED]
        #  action values are:
        #        1. Delete
        #        2. Release
        param_map['action'] = ['action for quarantine:', DEFAULT, 1]
        param_map['modify_subj'] = ['modify the subject', DEFAULT]
        # test_pos values are:
        #        1. Prepend
        #        2. Append
        param_map['text_pos'] = ['Select position of text.', DEFAULT, 1]
        param_map['text_to_add'] = ['Enter the text to add:', REQUIRED]
        param_map['add_header'] = ['add a custom header', DEFAULT]
        param_map['header_name'] = ['Enter the header name:', REQUIRED]
        param_map['header_content'] = ['Enter the header content', REQUIRED]
        param_map['strip_attachments'] = ['strip all attachments', DEFAULT]
        param_map['edit_user_roles'] = ['assign any user roles', DEFAULT]
        param_map['apply_quarantines'] = ['apply automatically when quarantine space fills up', DEFAULT]

        param_map.update(input_dict or kwargs)
        self._query_response('NEW')

        if kwargs.has_key('edit_user_roles'):
            if is_yes(kwargs['edit_user_roles']):
                self._process_input(param_map, do_restart=False)
                if _add_roles:
                    quarantineconfigUseuser(self._get_sess()).add(_add_roles)
                if _del_roles:
                    quarantineconfigUseuser(self._get_sess()).delete(_del_roles)
                return
        else:
            self._process_input(param_map)

    def edit(self, input_dict=None, **kwargs):
        _add_roles = kwargs.pop('add_roles', None)
        _del_roles = kwargs.pop('delete_roles', None)
        param_map = IafCliParamMap(end_of_command='Choose the operation')

        param_map['name'] = ['Enter the name or', REQUIRED]
        param_map['period'] = ['period for this quarantine', REQUIRED]
        #  action values are:
        #        1. Delete
        #        2. Release
        param_map['action'] = ['action for quarantine:', DEFAULT, 1]
        param_map['modify_subj'] = ['modify the subject', DEFAULT]
        # test_pos values are:
        #        1. Prepend
        #        2. Append
        param_map['text_pos'] = ['Select position of text.', DEFAULT, 1]
        param_map['text_to_add'] = ['Enter the text to add:', REQUIRED]
        param_map['add_header'] = ['add a custom header', DEFAULT]
        param_map['header_name'] = ['Enter the header name:', REQUIRED]
        param_map['header_content'] = ['Enter the header content', REQUIRED]
        param_map['strip_attachments'] = ['strip all attachments', DEFAULT]
        param_map['edit_user_roles'] = ['Do you want to edit any user roles',
                                        DEFAULT]
        param_map['apply_quarantines'] = ['apply automatically when quarantine space fills up', DEFAULT]
        param_map.update(input_dict or kwargs)
        self._query_response('EDIT')
        if kwargs.has_key('edit_user_roles'):
            if is_yes(kwargs['edit_user_roles']):
                self._process_input(param_map, do_restart=False)
                if _add_roles:
                    quarantineconfigUseuser(self._get_sess()).add(_add_roles)
                if _del_roles:
                    quarantineconfigUseuser(self._get_sess()).delete(_del_roles)
                return
        else:
            self._process_input(param_map)

    def delete(self, name=REQUIRED, confirm=YES):

        self._query_response('DELETE')
        self._query_response(name)
        # Confirmation to delete.
        # Are you sure you want to delete ..?
        self._query_response(confirm)
        self._to_the_top(self.newlines)

    def get_list_of_configured_quarantines(self, as_dictionary=YES):
        raw = self._read_until('allocated size for quarantines')
        self._restart_nosave()  # go to top-level command
        if is_no(as_dictionary):
            return raw
        quarantines = CfgHolder()
        tmp = raw.split('\n')
        for _tmp in tmp:
            res = _tmp.strip()
            if re.search('^\d+', res):
                quarantine_descr = re.split('\s{2,}', res)
                if len(quarantine_descr) >= 5:
                    name = quarantine_descr[1]
                    quarantines.__setattr__(name, CfgHolder())
                    quarantines['%s' % name]['space_used'] = quarantine_descr[2]
                    quarantines['%s' % name]['messages'] = quarantine_descr[3]
                    quarantines['%s' % name]['retention'] = quarantine_descr[4]
                    # quarantines['%s' % name]['action'] = quarantine_descr[5]
                    # some strange situation with 'Action' column,
                    # there is '\r\n' *before* and after it,
                    # so can't split neither by \n nor \r.
                    # also that will be problematic dur to long quarantine names
                    # which will cause CLI to print values for the same quarantine
                    # in new line
        return quarantines

    def get_space_available(self):
        raw = self._read_until('Choose the operation')
        self._restart_nosave()  # go to top-level command
        allocated_space = re.search('allocated size for quarantines is (\S+)\.', raw).group(1)
        used_space = re.search('used size is (\S+)', raw).group(1)
        return (self._convert_to_bytes(allocated_space) - \
                self._convert_to_bytes(used_space)) / 1073741824

    def _convert_to_bytes(self, size):
        value = size[:-1]
        unit = size[-1:]
        if unit.lower() == 'g':
            return float(value) * 1024 * 1024 * 1024
        if unit.lower() == 'm':
            return float(value) * 1024 * 1024
        if unit.lower() == 'k':
            return float(value) * 1024
        if unit.lower() == 'b':
            return float(value)

    def vofmanage(self):
        self._query_response('OUTBREAKMANAGE')
        # if there are no message in the outbreak quarantine
        # just return to the main prompt - you will have to catch
        # the AttributeError that will be thrown as a result of calling
        # delete() or release() on a NoneType though.
        self._expect(['There are no messages', 'Rule    '], timeout=2)
        if self._expectindex == 0:
            self._to_the_top(self.newlines)
        else:
            return quarantineconfigVofmanage(self._get_sess())


class quarantineconfigVofmanage(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    def __call__(self):
        return self

    def release(self, indicator):
        self._query_parse_input_list()
        self._writeln('RELEASE')
        self._query()
        self._select_list_item(indicator)
        self._expect(['RELEASE', 'Currently configured'])
        if self._expectindex == 0:
            self.newlines += 1
        self._to_the_top(self.newlines)

    def delete(self, indicator):
        self._query_parse_input_list()
        self._writeln('DELETE')
        self._query()
        self._select_list_item(indicator)
        self._expect(['RELEASE', 'Currently configured'])
        if self._expectindex == 0:
            self.newlines += 1
        self._to_the_top(self.newlines)


class quarantineconfigUseuser(clictorbase.IafCliConfiguratorBase):
    newlines = 2

    def __call__(self):
        return self

    def add(self, roles):
        self._writeln('NEW')
        self._writeln(roles)
        self._to_the_top(self.newlines)

    def delete(self, roles):
        self._writeln('DELETE')
        self._writeln(roles)
        self._to_the_top(self.newlines)


if __name__ == "__main__":
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()
    cli = quarantineconfig(cli_sess)

    # new testing:
    cli().new(name='test1', size='250', period='1', action='Delete')
    cli().new(name='test2', size='250', period='1', action='Release',
              sub_modifying=YES, test_pos='Prepend', text_to_add='test')
    cli().new(name='test3', size='250', period='1', action='Release',
              sub_modifying=YES, test_pos='Prepend', text_to_add='test',
              header_adding=YES, header_name='test', header_content='test',
              attach_stripping=NO)
    cli().new(name='test4', size='250', period='1', action='Release',
              sub_modifying=YES, test_pos='Prepend', text_to_add='test',
              header_adding=YES, header_name='test', header_content='test',
              attach_stripping=YES)

    # edit testing:
    cli().edit(name='test1', size='250', period='1', action='Delete')
    cli().edit(name='test1', size='250', period='1', action='Release',
               sub_modifying=YES, test_pos='Prepend', text_to_add='test')
    cli().edit(name='test1', size='250', period='1', action='Release',
               sub_modifying=YES, test_pos='Prepend', text_to_add='test',
               header_adding=YES, header_name='test', header_content='test',
               attach_stripping=NO)
    cli().edit(name='test1', size='250', period='1', action='Release',
               sub_modifying=YES, test_pos='Prepend', text_to_add='test',
               header_adding=YES, header_name='test', header_content='test',
               attach_stripping=YES)

    # delete testing:
    cli().delete('test1')
    cli().delete('test2')
    cli().delete('test3')
    cli().delete('test4')
