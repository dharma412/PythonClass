#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/outbreakupdate.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

import clictorbase
from clictorbase import IafCliError, IafCliConfiguratorBase
from sal.exceptions import ConfigError
from sal.deprecated.expect import REGEX
from sal.containers.yesnodefault import is_yes


class outbreakupdate(clictorbase.IafCliConfiguratorBase):
    class RequireActivationError(IafCliError):
        pass

    class OutbreakNotEnabled(IafCliError):
        pass

    def __init__(self, sess):
        IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
            ('This feature requires activation with a software key', REGEX): \
                self.RequireActivationError,
            ('Either IronPort Anti-Spam or Intelligent Multi-Scan or \
                          Outbreak Filters', REGEX): self.OutbreakNotEnabled,
        })

    def __call__(self, force=False):
        self.clearbuf()
        if is_yes(force):
            self._sess.writeln(self.__class__.__name__ + ' force')
        else:
            self._writeln(self.__class__.__name__)

        rv = self._query(
            self._get_prompt(),
            'Requesting updates for Outbreak Filter Rules.',
            'Forcing updates for Outbreak Filter Rules.')

        if not rv:
            raise ConfigError('Unexpected outbreakupdate response')

        self._wait_for_prompt()

        if rv == 1:
            return True


if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()
    cli = outbreakupdate(cli_sess)
    print cli(force=True)
    print cli()
