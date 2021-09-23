#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/ctor/publishconfig.py#1 $
"""IAF Command Line Interface (CLI) configurator: publishconfig
"""

import clictorbase

from sal.deprecated.expect import EXACT
from sal.exceptions import ConfigError


class publishconfig(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict(
            {('Invalid arguments when processing', EXACT): ConfigError,
             ('No such configuration master', EXACT): ConfigError,
             ('No WSA hosts', EXACT): ConfigError})

    def __call__(self, config_master, job_name=None, host_list=None):
        cmd_line = [self.__class__.__name__, config_master]

        if job_name is not None:
            cmd_line.append('--job_name=%s' % (job_name,))

        if host_list is not None:
            if isinstance(host_list, list):
                cmd_line.append('--host_list=%s' % (','.join(host_list),))
            else:
                cmd_line.append('--host_list=%s' % host_list)

        self._writeln(' '.join(cmd_line))
        self._expect('\n')
        return self._wait_for_prompt()


if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    cli = publishconfig(cli_sess)
    print cli('5.7', 'test_job', ('host1', 'host2'))
