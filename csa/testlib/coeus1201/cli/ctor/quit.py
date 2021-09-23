#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/quit.py#1 $
import clictorbase

from sal.exceptions import ExpectError

class quit(clictorbase.IafCliConfiguratorBase):
    def __call__(self, yes_or_no='yes'):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        try:
            idx = self._query('Are you sure you wish to exit?',
                         'Connection closed by foreign host',
                         'Connection to %s closed'%self._get_prompt().hostname)
        except ExpectError, e:
            if str(e).find('EOF during expect') >= 0:
                return True
            raise

        if idx == 0:
            yes_or_no = str(yes_or_no).strip().lower()
            self._writeln(yes_or_no)
            idx2 = self._query(self._get_prompt().single,
                              'Connection closed by foreign host',
                              'Connection to %s closed'%self._get_prompt().hostname)
            if idx2 == 0:
                return False
        del self._sess
        return True

if __name__ == '__main__':
    import sethostname
    from sal.containers.yesnodefault import YES, NO

    # session host defaults to .iafrc.DUT
    sess = clictorbase.get_sess()
    cli = quit(sess)
    # test case
    print 'do quit?', cli()
    sess = clictorbase.get_sess()
    sgw = sethostname.sethostname(sess)('bogushostname.com')
    cli = quit(sess)
    print 'do quit?', cli(NO)
