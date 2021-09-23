#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/grep.py#1 $
"""
IAF2 CLI command grep
"""

from sal.containers.yesnodefault import YES, NO, is_yes
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

    def __call__(self, log_name=REQUIRED, regex=DEFAULT, insensitive=DEFAULT, file_pattern='*'):
        self._writeln(self.__class__.__name__)
        self._query_select_list_item(log_name)
        self._query_response(regex)
        self._query_response(insensitive)
        # Do not tail logs
        self._query_response(NO)
        # Do not paginate output
        self._query_response(NO)
        # Define file pattern
        # mysterious option. how to define that pattern?
        self._query_response(file_pattern)
        self.clearbuf()
        return '\n'.join(self._wait_for_prompt().splitlines()[2:-1])

    def grep_batch(self,
                   regexp=None,
                   log_name=None,
                   count=NO,
                   count_around=None,
                   file_pattern=None,
                   ignore_case=NO,
                   paginate=NO,
                   tail=NO):
        # grep -e <regexp> [options] <log_name>
        # using only named arguments for easy perception
        cmd = '%s -e' % self.__class__.__name__
        if regexp is None:
            raise clictorbase.IafCliValueError \
                ('Regexp is required.')
        if log_name is None:
            raise clictorbase.IafCliValueError \
                ('Logname is required.')
        cmd += ' "%s"' % regexp
        if is_yes(count):
            cmd += " -c"
        if count_around:
            cmd += " -C %s" % count_around
        if file_pattern:
            cmd += " -f %s" % file_pattern
        if is_yes(ignore_case):
            cmd += " -i"
        if is_yes(paginate):
            cmd += " -p"
        if is_yes(tail):
            cmd += " -t"
        cmd += ' %s' % log_name
        self._sess.writeln(cmd)
        return self._sess.read_until()


if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    grep = grep(cli_sess)
    print grep(log_name='mail_logs', regex='Info: Begin Logfile')
