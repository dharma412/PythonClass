#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/ctor/grep.py#1 $
"""
IAF2 CLI command grep
"""

from sal.containers.yesnodefault import YES, NO
from sal.deprecated.expect import EXACT

import clictorbase

REQUIRED = clictorbase.REQUIRED
DEFAULT = clictorbase.DEFAULT


class NotFoundError(clictorbase.IafCliError): pass


class TailError(clictorbase.IafCliError): pass


class GrepError(clictorbase.IafCliError): pass


class grep(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ('No results were found', EXACT): NotFoundError,
            ('Unable to tail', EXACT): TailError,
            ('Unable to grep', EXACT): GrepError,
        })

    def __call__(self, log_name=REQUIRED, regex=DEFAULT, insensitive=DEFAULT):
        self._writeln(self.__class__.__name__)
        self._query_select_list_item(log_name)
        self._query_response(regex)
        self._query_response(insensitive)
        # Do not tail logs
        self._query_response(NO)
        # Do not paginate output
        self._query_response(NO)
        self.clearbuf()
        return '\n'.join(self._wait_for_prompt().splitlines()[2:-1])


if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    grep = grep(cli_sess)
    print grep(log_name='mail_logs', regex='Info: Begin Logfile')
