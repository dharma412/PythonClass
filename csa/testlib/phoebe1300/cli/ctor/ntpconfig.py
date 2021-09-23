#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/ntpconfig.py#1 $

"""
IAF 2 CLI command: ntpconfig
"""

import clictorbase


class ntpconfig(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self._writeln('ntpconfig')
        return self

    def new(self, server='time.ironport.com'):
        self.level = 1
        self._query_response('new')
        self._query_response(server)
        self._to_the_top(self.level)

    def delete(self, server):
        self.level = 1
        self._query_parse_input_list()
        self._writeln('delete')
        self._select_list_item(server)
        self._to_the_top(self.level)

    def sourceint(self, table='Auto'):
        self.level = 1
        self._query_response('sourceint')
        self._query_select_list_item(table)
        self._to_the_top(self.level)

    def get_ntp_info(self):
        """ Return list with currently configured NTPs.  """

        self.level = 1
        self._query()
        input_list_text_block = self._get_last_matched_text()
        info = self._input_list_obj.parse_text(input_list_text_block)
        self._to_the_top(self.level)
        return list(info.items())


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    ntpc = ntpconfig(cli_sess)
    ntpc().sourceint('Auto')
    ntpc().new('foo.bar.com')
    print ntpc().get_ntp_info()
    ntpc().delete('foo.bar.com')
