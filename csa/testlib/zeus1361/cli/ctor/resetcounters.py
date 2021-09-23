#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1360/cli/ctor/resetcounters.py#1 $ $DateTime: 2020/03/05 19:45:32 $ $Author: sarukakk $
import clictorbase
class resetcounters(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self._writeln('resetcounters')
        self._query('Counters ')
        self._wait_for_prompt()
if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()
    rcout = resetcounters(cli_sess)
    rcout()
    print 'resetcounters test DONE!'
