#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/hostrate.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

"""
CLI command: hostrate
"""

import re
import time

import sal.time

from deleterecipients import deleterecipients
from clictorbase import IafCliConfiguratorBase, IafCliParamMap, get_sess, \
    IafIpHostnameError, REQUIRED, DEFAULT, IafCliValueError
from sal.deprecated.expect import EXACT
from sal.exceptions import ConfigError


class Records:

    def __init__(self, rate_recs, start_pos):

        # Result list
        self.result = []

        # For example we have hostrate record:
        # 11:27:15   unknown      0       0       0       0       0       0
        #
        # Patterns:
        #
        # Group 1 (\d\d:\d\d:\d\d) - to retrieve time
        # Group 2 ([a-z]+)         - to retrive host status
        # Group 3 (-?\d+\s+-?\d+\s+-?\d+\s+-?\d+\s+-?\d+\s+-?\d+) - to retrieve
        #                                            the values of the counters
        pattern = re.compile('(\d\d:\d\d:\d\d)\s+'
                             '([a-z]+)\s+'
                             '(-?\d+\s+-?\d+\s+-?\d+\s+-?\d+\s+-?\d+\s+-?\d+)')

        # Hostrate counters
        self.counters = ['Time', \
                         'Host Status', \
                         'CrtCncOut', \
                         'ActvRcp', \
                         'ActvRcp Delta', \
                         'DlvRcp Delta', \
                         'HrdBncRcp Delta', \
                         'SftBncEvt Delta']

        # Skip past the next start_pos lines to reach the rate data:
        # [10]>
        #
        # Type Ctrl-C to return to the main prompt.
        #
        #    Time      Host  CrtCncOut   ActvRcp ActvRcp  DlvRcp \
        #             Status                       Delta   Delta \
        # 11:27:15   unknown         0         0       0       0 \
        # HrdBncRcp  SftBncEvt
        #     Delta     Delta
        #         0         0
        rate_rects_cleared = rate_recs[start_pos:len(rate_recs) - 1]

        # Processing
        for rate_rec in rate_rects_cleared:
            result = pattern.search(rate_rec)
            if result:
                record = [result.group(1), result.group(2)] + \
                         self.extract_digits(result.group(3))
                self.result.append(record)

    def extract_digits(self, x):
        """Return list based on retrieved counters"""
        return map(int, re.split(r'\s+', x.strip()))

    def get_value(self, rec_idx, counter):
        """Return counter by name and row number"""

        if counter not in self.counters:
            return None

        return self.result[rec_idx][self.counters.index(counter)]


class hostrate(IafCliConfiguratorBase):

    def __init__(self, sess):

        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ("Couldn't obtain hostrate stats.",
             EXACT): IafCliValueError,
        })

    def __call__(self, batch=False, records=2, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Type Ctrl-C to return')

        params = input_dict or kwargs
        self._sess.clearbuf()

        if batch:
            host = params.get('host')
            if host is None:
                raise ConfigError('Host is required argument when ' \
                                  'running command in batch mode')
            sec = params.get('sec', '')
            cmd = 'hostrate %s %s' % (host, sec)
            self._writeln(cmd)
            start_pos = 6
        else:
            self._writeln('hostrate')
            param_map['host'] = ['Recipient host:', REQUIRED]
            param_map['sec'] = ['Enter the number of seconds', DEFAULT]
            param_map.update(params)
            self._process_input(param_map, do_restart=False)
            start_pos = 4

        sleep_val = int(records) * int(params.get('sec') or 10)

        timer = sal.time.CountDownTimer(sleep_val).start()
        while timer.is_active():
            time.sleep(1)

        self._sess.interrupt()
        out = self._read_until('^C').split('\n')

        # Sometimes the appliance does not react for the first Ctrl-C.
        # restart_nosave will send Ctrl-C 10 more times.
        self._restart_nosave(0.5)

        return '\n'.join(out[start_pos:])


if __name__ == '__main__':
    from clictorbase import get_sess

    sess = get_sess()
    hr = hostrate(sess)
    records = hr(records=5, host='mail.qa', sec=3)
    print 'Result of the hostrate execution:'
    print records.result

    records = hr(batch=True, records=5, host='mail.qa', sec=4)
    print 'Result of the hostrate execution in batch mode:'
    print records.result
