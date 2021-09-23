# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/ecupdate.py#1 $ $DateTime: 2019/03/22 01:36:06 $Author: rahugup4 $

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
