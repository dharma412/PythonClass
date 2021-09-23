#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1250/cli/ctor/resetcounters.py#3 $ $DateTime: 2019/06/07 02:45:52 $ $Author: sarukakk $
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
