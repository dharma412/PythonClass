# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/ecstatus.py#1 $ $DateTime: 2019/06/27 23:26:24 $Author: rahugup4 $

import clictorbase


class ecstatus(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        cmd = 'ecstatus'
        self._sess.writeln(cmd)
        return self.ecstatus_parse(self._read_until())

    def ecstatus_parse(self, ecstatus_str):
        return ecstatus_str


if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    ec = ecstatus(cli_sess)
    ec_str = ec()
