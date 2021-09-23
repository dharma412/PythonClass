#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/settime.py#1 $


from sal.exceptions import ConfigError
from sal.exceptions import TimeoutError
from sal.containers.yesnodefault import YES, NO
import time

import clictorbase


class settime(clictorbase.IafCliConfiguratorBase):

    def __call__(self, timeval=None, shutdown_ntp=YES):
        """Sets the system time. May turn off NTP if shutdownNTP is YES. If the
        timeval is None then just return the current time without setting it.
        The timeval may also be a time tuple (see module 'sal.time'). Returns
        the old and the new time.
        """

        import re
        import time
        import sal.time

        tvt = type(timeval)
        if tvt is tuple or tvt is time.struct_time or \
                tvt is sal.time.MutableTime:
            timeval = time.strftime("%m/%d/%Y %H:%M:%S", timeval)

        self._writeln('settime')
        # if no time value is specified just
        # grab the current system time and return it
        if not timeval:
            ii = self._query('stop NTP', 'enter the time')
            if ii == 0:
                self._query_response(YES)
                self._read_until('enter the time')

            self.interrupt()
            self._writeln()
            cur_time = re.findall('Current time (.+)\.\r\n', self.getbuf())
            if not cur_time:
                raise ConfigError, 'Error in parsing settime output'
            return cur_time[-1]

        ii = self._query('stop NTP', 'enter the time')
        if ii == 0:
            self._query_response(shutdown_ntp)
            time.sleep(5)
        self._query_response(timeval)
        try:
            self._wait_for_prompt()
        except TimeoutError, e:
            print 'settime failed. unable to find main prompt.'
            self._sess.interrupt()
            raise


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    st = settime(cli_sess)
    print st()

    t = '11/20/2005 15:50:50'  # MM/DD/YYYY HH:MM:SS
    # test with t
    print 'positive test case:test with time format string'
    st(t)
    # negative test case
    t = 'Sun Nov 20 15:50:50 2005 PST'
    try:
        st(t)
    except TimeoutError, te:
        print 'Timeout error found, as expected in negative test case'
    print 'Settime test done!'
