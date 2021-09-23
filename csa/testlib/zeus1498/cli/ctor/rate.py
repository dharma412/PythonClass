#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1380/cli/ctor/rate.py#1 $

"""
IAF 2 CLI command: rate
"""

import re
import time

import sal.time

from clictorbase import IafCliConfiguratorBase, IafCliParamMap, get_sess,\
    DEFAULT, IafCliValueError
from sal.deprecated.expect import EXACT


class Records:

    def __init__(self, rate_recs, start_pos):

        # Result list
        self.result = {}

        # For example we have rate record:
        # 01:36:30     0     0        7      0       6     0    323
        #
        # Patterns:
        #
        # Group 1 (\d\d:\d\d:\d\d) - to retrieve time
        # Group 2 (-?\d+\s+-?\d+\s+-?\d+\s+-?\d+\s+-?\d+\s+-?\d+\s+-?\d+) -
        #          to retrieve the values of the counters
        pattern = re.compile('(\d\d:\d\d:\d\d)\s+'
                             '(-?\d+\s+-?\d+\s+-?\d+\s+-?\d+\s+-?\d+\s+-?\d+\s+-?\d+)')

        # Rate counters
        self.counters = ['Time', \
                         'Connections In', \
                         'Connections Out', \
                         'Recipients Recieved', \
                         'Recieved Delta', \
                         'Recipients Completed', \
                         'Completed Delta',\
                         'Queue K-Used']


        # Skip past the next start_pos lines to reach the rate data:
        # [10]>
        #
        # Type Ctrl-C to return to the main prompt.
        #
        #  Time    Connections Recipients          Recipients            Queue
        #           In   Out   Received    Delta   Completed    Delta    K-Used
        # 01:36:30   0     0          7        0          6         0     323
        rate_rects_cleared = rate_recs[start_pos:len(rate_recs)-1]

        # Processing
        for rate_rec in rate_rects_cleared:
            result = pattern.search(rate_rec)
            if result:
                self.result[result.group(1)] =\
                    self.extract_digits(result.group(2))

    def extract_digits(self, x):
        """Return list based on retrieved counters"""
        return map(int, re.split(r'\s+', x.strip()))

    def get_value(self, rec_idx, counter):
        """Return counter by name and row number"""

        if counter not in self.counters:
            return None

        return self.result[rec_idx][self.counters.index(counter)]


class rate(IafCliConfiguratorBase):

    def __init__(self, sess):

        IafCliConfiguratorBase.__init__(self, sess)
        self._set_local_err_dict({
            ("Couldn't obtain rate stats.",
                                       EXACT) : IafCliValueError,
            })

    def __call__(self, batch=False, records=2, input_dict=None, **kwargs):
        param_map = IafCliParamMap(end_of_command='Type Ctrl-C to return')
        params = input_dict or kwargs
        self._sess.clearbuf()

        if batch:
            sec = params.get('sec', '10')
            cmd = 'rate %s' % (sec,)
            self._writeln(cmd)
            start_pos = 6
        else:
            self._writeln('rate')
            param_map['sec']  = ['Enter the number of seconds', DEFAULT]
            param_map.update(params)
            self._process_input(param_map, do_restart=False)
            start_pos = 4

        sleep_val = records * int(params.get('sec', 10))

        timer = sal.time.CountDownTimer(sleep_val).start()
        while timer.is_active():
            time.sleep(1)

        self._sess.interrupt()
        out = self._read_until('^C').split('\n')

        # Sometimes the appliance does not react for the first Ctrl-C.
        # restart_nosave will send Ctrl-C 10 more times.
        self._restart_nosave(0.5)
        return Records(out, start_pos).result

if __name__ == '__main__':
    from clictorbase import get_sess
    sess = get_sess()
    r = rate(sess)
    records = r(records=5, sec=3)
    print 'Result of the rate execution:'
    print records.result

    records = r(batch=True, records=5, sec=4)
    print 'Result of the rate execution in batch mode:'
    print records.result

