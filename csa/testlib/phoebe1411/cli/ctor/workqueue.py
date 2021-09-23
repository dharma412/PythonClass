#!/usr/bin/env python

"""
IAF2 Command Line Interface (CLI)
command: - workqueue
"""
import clictorbase

from sal.exceptions import ConfigError
import re
import time
from sal.deprecated.expect import REGEX, EXACT
from sal.containers.yesnodefault import YES, NO, is_yes, is_no

class workqueue(clictorbase.IafCliConfiguratorBase):
    """"""
    def __call__(self):
        self._writeln('workqueue')
        return self

    def pause(self, confirm=YES, reason='IAF2 configurator'):
        self._query_response('pause')
        self._query_response(confirm)

        if is_yes(confirm):
            self._query_response(reason)

        self._restart()

    def resume(self):
        try:
            self._resume()
        except clictorbase.IafUnknownOptionError, ioe:
            self._restart()

    def _resume(self):
        self._query_response('resume')
        self._restart()

    def rate(self, delay=5, period=1):
        self.clearbuf()
        self._query_response('rate')
        self._query_response(delay)
        # Verify if the value has been accepted
        self._expect('Type Ctrl-C')
        time.sleep(period)
        self._sess.interrupt()
        self._expect('Choose the operation')
        resplist = r'\d\d:\d\d:\d\d +(\d+) +(\d+) +(\d+)'
        buf = self.getbuf()
        rate_list = re.findall(resplist, buf)

        rate_obj_list = []

        if rate_list:
            for item in rate_list:
                rate_obj_list.append(workqueueRate(
                    pending_rate = item[0],
                    in_rate = item[1],
                    out_rate = item[2],
                ))

        else:
            raise ConfigError, 'Output of the rate command can not be parsed'

        return rate_obj_list


    def status(self):
        self._query_response('status')

        resplist = [(r'Status:\s+(.+)\nMessages:\s+(\d+)\r\n', REGEX)]
        mo = self._expect(resplist, timeout=60)

        if mo:
            status = mo.group(1)
            num_workqueue_msgs = int(mo.group(2))
            status_of_workqueue = mo.group(1)
            self._to_the_top(1)
            return workqueueStatus(status_of_workqueue, num_workqueue_msgs)

        else:
            # Failed to get work queue status
            self._to_the_top(1)
            raise ConfigError, "Couldn't parse output from workqueue command"


class workqueueStatus:
    def __init__(self, status='', messages=0):
        self.status = status
        self.messages = messages

    def __str__(self):
        return 'Status:   %s\nMessages: %s' %(self.status, self.messages)

class workqueueRate:
    def __init__(self, pending_rate, in_rate, out_rate):
        self.pending_rate = pending_rate
        self.in_rate = in_rate
        self.out_rate = out_rate

if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    wq = workqueue(cli_sess)
    wq().pause()
    print wq().status()

    wq().resume()
    wr = wq().rate(2, 1)
    print 'pending:', wr[0].pending_rate
    print 'in:     ', wr[0].in_rate
    print 'out:    ', wr[0].out_rate
    ws = wq().status()
    print 'Workqueue status:  ', ws.status
    print 'Workqueue messages:',ws.messages

