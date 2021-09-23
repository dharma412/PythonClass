#!/usr/bin/env python

"""
IAF 2 CLI command: rollovernow
"""
import clictorbase

class rollovernow(clictorbase.IafCliConfiguratorBase):
    def __call__(self, logfile='All Logs'):
        self._sess.writeln('rollovernow')
        self._query_select_list_item(logfile)
        self._wait_for_prompt()

if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    rollnow = rollovernow(cli_sess)
    rollnow(logfile=1)
    rollnow(logfile='mail')

