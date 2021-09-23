#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/ctor/resumedel.py#1 $ $DateTime: 2019/09/18 01:46:35 $ $Author: sarukakk $
import clictorbase

from sal.exceptions import ConfigError


class resumedel(clictorbase.IafCliConfiguratorBase):

    def __call__(self):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        no = self._query('Mail delivery resumed',
                         'cannot resume')
        if no == 0:
            self._wait_for_prompt()
            return True
        elif no == 1:
            raise ConfigError, "%s: delivery could not be resumed" \
                               % self.__class__.__name__
        else:
            raise ConfigError, "%s command execution error" \
                               % self.__class__.__name__


if __name__ == '__main__':
    # session host defaults to .iafrc.DUT
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    cli = resumedel(cli_sess)
    print cli()
