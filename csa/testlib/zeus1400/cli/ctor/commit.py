#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/commit.py#1 $
"""IAF Command Line Interface (CLI) configurator: commit
"""

import clictorbase as ccb
from sal.exceptions import ConfigError

class commit(ccb.IafCliConfiguratorBase):
    def __call__(self, comments='IAF2 configurator', discard=ccb.DEFAULT):
        self.clearbuf()
        self._writeln(self.__class__.__name__)
        if self._query('enter some comments describing your changes:',
                    'no data to commit.') == 0:
            self._writeln(str(comments))
            if self._query('Are you ready to discard all of your changes?',
                            self._get_prompt(),timeout=120) == 0:
                self._writeln(discard)
                self._wait_for_prompt()
                return True

            else:
                if discard != ccb.DEFAULT:
                    raise ConfigError('Unanswered question')
                return True

        else:
            self._wait_for_prompt(timeout=120)
            return False

if __name__ == '__main__':
    from iafframework import iafcfg
    my_host = iafcfg.get_hostname()

    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()
    import sethostname

    cli = commit(cli_sess)
    print cli()
    shn = sethostname.sethostname(cli_sess)
    shn('newhost.%s' % my_host)
    cli = commit(cli_sess)
    print cli()
    shn(my_host)
    print cli('commit test')
