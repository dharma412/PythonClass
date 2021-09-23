# !/usr/bin/python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/clear.py#1 $

import clictorbase as ccb
from sal.containers.yesnodefault import YES, NO

class clear(ccb.IafCliConfiguratorBase):
    def __call__(self, confirm_clear_changes = YES):
        self._writeln(self.__class__.__name__)
        idx = self._query(self._sub_prompt, 'No changes have been made')
        
        if idx == 0:
            # Clear changes
            self._writeln(confirm_clear_changes)
            self._wait_for_prompt()
            return True
        elif idx == 1:
            # No Changes have been made
            self._wait_for_prompt()
            return False
        else:
            # should never reach this line of code
            raise RuntimeError, "clear CLI command failed"

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

    shn = sethostname.sethostname(cli_sess)
    shn('newhost.%s' % my_host)
    cli = clear(cli_sess)
    # test cases
    print cli(NO)
    print cli(YES)
    print cli()


