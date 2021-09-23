#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/exceptionconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

"""
SARF CLI command: exceptionconfig
"""
import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliValueError, \
    DEFAULT, REQUIRED, IafCliCtorNotImplementedError

from sal.deprecated.expect import EXACT
from sal.containers.yesnodefault import YES, NO, is_yes


class exceptionconfig(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    def __init__(self, sess):
        try:
            IafCliConfiguratorBase.__init__(self, sess)
        except NameError:
            self.IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('Any of the following passes:', EXACT): IafCliValueError,
            ('Parse error on address:', EXACT): IafCliValueError,
            ('An email address is a localname followed by the', EXACT): \
                IafCliValueError,
            ('Neither source nor target indices may be larger' \
             ' then the size of the table and must be positive.', \
             EXACT): IafCliValueError,
            ('The SMTP code must be a', EXACT): IafCliValueError,
        })

    def __call__(self):
        self._writeln(self.__class__.__name__)
        return self

    def _check_policy(self,
                      policy,
                      use_smtp_custom_code,
                      smtp_code,
                      smtp_rsp):
        """Shared function for new and edit commads common functionality"""
        # the policy values are:
        #               1. Allow
        #               2. Reject

        i = self._query_select_list_item(policy)
        if i == 2:
            self._query_response(use_smtp_custom_code)
            if is_yes(use_smtp_custom_code):
                self._query_response(smtp_code)
                self._query('custom SMTP response')
                self._writeln(smtp_rsp)
            self._writeln()
            self._writeln()
        self._to_the_top(newlines=2)

    def new(self,
            address=REQUIRED,
            policy=DEFAULT,
            use_smtp_custom_code=DEFAULT,
            smtp_code=DEFAULT,
            smtp_rsp=REQUIRED):
        self._query_response('NEW')
        self._query_response(address)
        self._check_policy(policy, use_smtp_custom_code, smtp_code, smtp_rsp)

    def edit(self,
             address=REQUIRED,
             new_address=REQUIRED,
             policy=DEFAULT,
             use_smtp_custom_code=DEFAULT,
             smtp_code=DEFAULT,
             smtp_rsp=REQUIRED):
        self._query_response('EDIT')
        self._query_select_list_item(address)
        self._query_response(new_address)
        self._check_policy(policy, use_smtp_custom_code, smtp_code, smtp_rsp)

    def delete(self, address):
        self._query_response('DELETE')
        self._query_select_list_item(address)
        self._to_the_top(self.newlines)

    def print_exception_table(self):
        import re
        self._query_response('PRINT')
        raw = self._read_until('Choose the operation ')
        self._to_the_top(newlines=1)
        res = re.search(r'(Domain Exception.*)', raw, re.DOTALL)
        return res.group(1)

    # search returns TRUE if pointed mail was found
    # otherwise returns FALSE
    def search(self, address):
        self._query_response('SEARCH')
        self._query_response(address)
        if self._query('Domain', 'There is no entry which matches') == 0:
            self._to_the_top(self.newlines)
            return 1
        else:
            self._to_the_top(self.newlines)
            return 0

    def move(self,
             entry_to_move=REQUIRED,
             dst_entry=REQUIRED):
        self._query_response('MOVE')
        self._query_select_list_item(entry_to_move)
        self._query_select_list_item(dst_entry)
        self._to_the_top(self.newlines)

    def clear(self, confirm=YES):
        self._query_response('CLEAR')
        # confirmation  to clear.
        # Are you sure you want to clear all domain exceptions?
        self._query_response(confirm)
        self._to_the_top(self.newlines)

    def clusterset(self):
        raise IafCliCtorNotImplementedError

    def clustershow(self):
        raise IafCliCtorNotImplementedError


if __name__ == "__main__":
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    cli = exceptionconfig(cli_sess)
    # testing new:
    cli().new(address='test@partial.domain')
    cli().new(address='test@partial.domain1', policy='Reject', \
              use_smtp_custom_code=YES, smtp_code='555', smtp_rsp='test')
    cli().new(address='test@partial.domain2', policy='Reject', \
              use_smtp_custom_code=NO)
    # testing edit:
    cli().edit(old_address='test@partial.domain', \
               new_address='test@partial.domain3')
    cli().edit(old_address='test@partial.domain1', \
               new_address='test@partial.domain4', policy='Reject', \
               use_smtp_custom_code=YES, smtp_code='555', smtp_rsp='test')
    cli().edit(old_address='test@partial.domain2', \
               new_address='test@partial.domain5', policy='Reject', \
               use_smtp_custom_code=NO, smtp_code='555', smtp_rsp='test')
    # testing delete:
    cli().delete('test@partial.domain')
    # testing print:
    cli().print_exception_table()
    # testing search:
    print cli().search('test@partial.domain1')
    print cli().search('test@partial.domain4')
    # testing move:
    cli().move(entry_to_move='test@partial.domain4', \
               dst_entry='test@partial.domain4')
    cli().move(entry_to_move='test@partial.domain4', \
               dst_entry='test@partial.domain5')
    # testing clear:
    cli().clear(YES)
