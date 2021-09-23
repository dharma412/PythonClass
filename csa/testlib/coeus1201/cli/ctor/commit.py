#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/commit.py#1 $
import clictorbase
from sal.exceptions import TimeoutError, ExpectError


class commit(clictorbase.IafCliConfiguratorBase):

    def __call__(self, comments='IAF2 configurator', rollback_option='N'):
        self._writeln('commit')
        ret_val = False
        if self._query('lease enter some comments', 'no data to commit') == 0:
            self._writeln(str(comments))
            try:
                if self._query("Do you want to save the current configuration for rollback? [Y]>") == 0:
                    self._writeln(str(rollback_option))
                    ret_val = True
            except TimeoutError:
                print ('Rollback option did not appear. It may not exist.')
                self._writeln()

        self._wait_for_prompt(60)
        return ret_val

if __name__ == '__main__':
    import antispamconfig
    sess = clictorbase.get_sess()
    asc = antispamconfig.antispamconfig(sess)
    asc(vendor='ironport').setup(license_agreement='y')
    cli = commit(sess)
    # test case
    print cli()
    print cli('commit test')
