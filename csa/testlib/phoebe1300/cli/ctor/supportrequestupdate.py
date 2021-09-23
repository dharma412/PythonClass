# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/supportrequestupdate.py#1 $
# $DateTime: 2019/06/27 23:26:24 $
# $Author: aminath $

import clictorbase
from clictorbase import IafCliError, IafCliConfiguratorBase
from sal.exceptions import ConfigError


class supportrequestupdate(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self, force=False):
        self.clearbuf()
        if force:
            self._writeln(self.__class__.__name__ + ' force')
        else:
            self._writeln(self.__class__.__name__)

        status_output = self._wait_for_prompt()
        output = [y for y in (x.strip() for x in status_output.splitlines()) if y]
        return output[1]


if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()
    cli = supportrequestupdate(cli_sess)
    print cli(force=True)
    print cli()
