#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/addresslistconfig.py#1 $
# $Date: 2019/03/22 $
# $Author: aminath $

import clictorbase
from clictorbase import REQUIRED, DEFAULT


class addresslistconfig(clictorbase.IafCliConfiguratorBase):
    newlines = 1

    def __call__(self):
        self._writeln('addresslistconfig')
        return self

    def new(self, list_name=REQUIRED, list_desc=DEFAULT, list_type=DEFAULT,
            addr_list=DEFAULT):
        self._query_response('NEW')
        self._query_response(list_name)
        self._query_response(list_desc)
        self._query_select_list_item(list_type)
        self._query_response(addr_list)
        self._to_the_top(self.newlines)

    def edit(self, list_name=REQUIRED, new_list_name=DEFAULT, list_desc=DEFAULT,
             addr_list=DEFAULT):
        self._query_response('EDIT')
        self._query_select_list_item(list_name)
        self._query_response(new_list_name)
        self._query_response(list_desc)
        self._query_response(addr_list)
        self._to_the_top(self.newlines)

    def Print(self, list_name=DEFAULT):
        self._query_response('PRINT')
        self._query_select_list_item(list_name)
        self._expect('\n')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.newlines)
        return raw

    def delete(self, list_name=DEFAULT):
        self._query_response('DELETE')
        self._query_select_list_item(list_name)
        self._to_the_top(self.newlines)

    def conflicts(self, list_name=DEFAULT):
        self._query_response('CONFLICTS')
        self._query_select_list_item(list_name)
        self._query('\n')
        raw = self._read_until('Choose the operation')
        self._to_the_top(self.newlines)
        return raw


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    addr_cfg = addresslistconfig(cli_sess)

    addr_cfg().new(list_name='test',
                   list_desc='MyTest',
                   addr_list='@a.com,@b.com')
    addr_cfg().edit(list_name='test', new_list_name='newtest',
                    addr_list='@c.com')
    print addr_cfg().Print(list_name='newtest')
    print addr_cfg().conflicts(list_name='newtest')
    addr_cfg().delete(list_name='newtest')
    print 'addrlistconfig test PASSED!'
