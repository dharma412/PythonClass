#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/reboot.py#1 $

import clictorbase
import time
from sal.containers.yesnodefault import YES, NO

class reboot(clictorbase.IafCliConfiguratorBase):
    def __call__(self, wait_secs=30, confirm_continue=YES, just_return=None):

        self._writeln('reboot')

        if self._query('re you sure', self._sub_prompt) == 0:
            self._query_response(confirm_continue)
            if not confirm_continue:
                self._to_the_top(1)
                return
            self._query_response(wait_secs)
        else:
            # sub_prompt has already matched in the query() call
            self._writeln(wait_secs)

        if just_return:
            return
        else:
            # jcc added sleep to temporary overcome C60 bug 3128.
            # adaptive sleep: wait 10s after shutdown of processes is initiated
            time.sleep(int(wait_secs) + 10)
            self.close()

if __name__ == '__main__':
    from sal.net import ping
    import sal.net.socket
    from iafframework import iafcfg

    sess = clictorbase.get_sess() # session host defaults to .iafrc.DUT
    host = iafcfg.get_hostname()

    rt = reboot(sess)

    print 'set gateway'
    # uncommitted setgateway
    rt._writeln('setgateway')
    rt._query_response('172.17.0.2')
    rt._wait_for_prompt()

    print 'reboot 1'
    # postiive test case. Do nothing
    rt(5, NO)
    sal.net.socket.wait_for_port(host, 22, 1)

    print 'reboot 2'
    # postiive test case. Reboot with changes
    rt(5, YES)
    ping.wait_for_reboot(host)
    sal.net.socket.wait_for_port(host, 22)

    print 'reboot 3'
    # reboot with no changes
    sess2 = clictorbase.get_sess() # session host defaults to .iafrc.DUT
    rt = reboot(sess2)
    rt(3)
    ping.wait_for_reboot(host)
    sal.net.socket.wait_for_port(host, 22)

    print 'reboot 4'
    sess3 = clictorbase.get_sess() # session host defaults to .iafrc.DUT
    # negative test case
    rt = reboot(sess3)
    rt(-1)

