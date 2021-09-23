#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/resume.py#1 $

"""
IAF 2 Command Line Interface (CLI)

command:
    - resume
"""
import clictorbase

from sal.exceptions import ConfigError


class resume(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        no = self._query('Receiving resumed for',
                         'No listeners were resumed.',
                         'cannot resume')
        if no == 0:
            self._wait_for_prompt()
            return True
        elif no == 1:
            self._wait_for_prompt()
            return False
        elif no == 2:
            raise ConfigError, "%s: could not resume receiving" \
                               % self.__class__.__name__
        else:
            raise ConfigError, "%s command executed error" \
                               % self.__class__.__name__


if __name__ == '__main__':
    import suspend

    # session host defaults to .iafrc.DUT
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    cli = resume(cli_sess)
    print "Suspend without resume should return False: " + str(cli())
    # suspend delivery first
    suspend.suspend(cli_sess)(5)
    # test case
    print "Suspend without resume should return True: " + str(cli())
