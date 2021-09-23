# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/ecupdate.py#1 $ $DateTime: 2020/01/06 01:25:43 $Author: rahugup4 $

import clictorbase

class ecupdate(clictorbase.IafCliConfiguratorBase):
    def __call__(self, force=False):
        cmd = 'ecupdate'
        if force:
            cmd += ' force'
        self._sess.writeln(cmd)
        self._wait_for_prompt()

if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    un = ecupdate(cli_sess)
    un()
