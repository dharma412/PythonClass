#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/status.py#1 $
"""
IAF Command Line Interface (CLI)
command: - status
"""

import copy
import re

from sal.containers import cfgholder
import clictorbase

class status(clictorbase.IafCliConfiguratorBase):
    def __call__(self, detail_bool=True):
        cmd = 'status'
        if detail_bool:
            cmd += ' detail'
        # run status CLI command
        self._writeln(cmd)
        # status can be slow in responding if the mga is under heavy load.
        status_output = self._wait_for_prompt(timeout=180)

        # check for error
        if status_output.find("Couldn't obtain mail stats") >= 0 \
                or status_output.find("Unknown option") >= 0:
            raise clictorbase.IafCliError, status_output

        # parse CLI command output and return a status object
        return StatusInfoObject(status_output)

class StatusInfoCounter(list):
    """An object representing a line of output of the status CLI command.
    The line of output is represented by self.pattern.
    self.pattern can contain %s and %d to represent strings and integers.
    The %s and %d will be extracted from the status_output class attribute.
    Two examples of self.pattern:
        1. self.pattern = 'Up since:                      %s (%s)'
        2. self.pattern = '    Filter Hard Bounces   %d %d %d'
    """
    status_output = ''
    def __init__(self, pattern):
        super(self.__class__, self).__init__(self)

        self.pattern = self.orig_pattern = pattern
        self._parse()

    def _reformat_pattern(self):
        # Should probably translate more special regex characters
        # to handle all cases but this minimal set is sufficient to handle
        # current status output.
        self.pattern = self.pattern.replace('(', '\(')      # escape parens
        self.pattern = self.pattern.replace(')', '\)')      # escape parens
        self.pattern = self.pattern.replace('%s', '\s*(.*)')# %s: string
        self.pattern = self.pattern.replace('%d', '\s*(\S+)\s*')#%d: integer
        self.pattern = self.pattern.replace('%%', '%')      # %%: percent sign

    def _parse(self):
        self._reformat_pattern()
        m = re.search(self.pattern, self.status_output)
        if not m:
            return

        self[:] = [] # reinitialize list to an empty list
        for match_value in map(lambda s: s.strip(), m.groups()):
            self.append(match_value)

class StatusInfoObject:
    """Object representing the output of the status CLI command.
    Status information is broken up and placed into 1 category:

        self.system:    Any info  before the "Counters:" section

    Note the name of the object attribute maps very closely to the name
    of the name of the field name displayed by the status command.
    Example:
        status_as_of -> 'Status as of:                       %s'
    """
    def __init__(self, status_output):
        self.system       = cfgholder.CfgHolder()
        self.transactions = cfgholder.CfgHolder()
        self.bandwidth    = cfgholder.CfgHolder()
        self.response     = cfgholder.CfgHolder()
        self.hit_rate     = cfgholder.CfgHolder()
        self.connections  = cfgholder.CfgHolder()

        ti = status_output.find('Transactions per Second')
        bi = status_output.find('Bandwidth')
        ri = status_output.find('Response Time')
        hi = status_output.find('Cache Hit Rate')
        ci = status_output.find('Connections')

        system_out = status_output[:ti]
        transactions_out = status_output[ti:bi]
        bandwidth_out = status_output[bi:ri]
        response_out = status_output[ri:hi]
        hit_rate_out = status_output[hi:ci]
        connections_out = status_output[ci:]

        configuration = {}

        # SYSTEM
        configuration[('self.system',system_out)]={
        'status_as_of':             'Status as of:                  %s',
        'up_since':                 'Up since:                      %s (%s)',
        }

        # Transactions per Second
        configuration[('self.transactions', transactions_out)]={
        'ave_last_minute':          'Average in last minute         %d',
        'max_last_hour':            'Maximum in last hour           %d',
        'ave_last_hour':            'Average in last hour           %d',
        'max_since_restart':        'Maximum since proxy restart    %d',
        'ave_since_restart':        'Average since proxy restart    %d',
        }

        configuration[('self.bandwidth', bandwidth_out)] =\
            copy.deepcopy(configuration[('self.transactions', transactions_out)])

        configuration[('self.response', response_out)] =\
            copy.deepcopy(configuration[('self.transactions', transactions_out)])

        configuration[('self.hit_rate', hit_rate_out)] =\
            copy.deepcopy(configuration[('self.transactions', transactions_out)])

        configuration[('self.connections', connections_out)]={
        'idle_client':              'Idle client connections        %d',
        'idle_server':              'Idle server connections        %d',
        'total_client':             'Total client connections       %d',
        'total_server':             'Total server connections       %d',
        }

        for out_tuple, var2patt_dict in configuration.items():
            attribute_holder, partial_status_output = out_tuple
            StatusInfoCounter.status_output = partial_status_output
            for var_name, pattern in var2patt_dict.items():
                s='%s["%s"]=StatusInfoCounter(pattern)'%\
                        (attribute_holder,var_name)
                exec(s)

    def __str__(self):
        s = []
        s.append('STATUS:'+str(self.system))
        s.append('TRANSACTIONS:'+str(self.transactions))
        s.append('BANDWIDTH:'+str(self.bandwidth))
        s.append('RESPONSE:'+str(self.response))
        s.append('HIT RATE:'+str(self.hit_rate))
        s.append('CONNECTIONS:'+str(self.connections))
        return '\n'.join(s)

    def get_system(self, name, idx=0):
        # name can be:
        #   status_as_of up_since
        # idx:
        #   up_since has 2 values. So idx can be 0 or 1 for this attribute.
        #   idx must be zero for every other 'name'.
        # Returns:
        #   A string.
        assert (name == 'up_since' and idx in (0,1)) or (idx == 0)
        return self.system[name][idx]

    def get_transactions(self, name):
        # name can be:
        #   ave_last_minute max_last_hour ave_last_hour max_since_restart
        #   ave_since_restart
        # Returns:
        #  A string.
        return self.transactions[name][0]

    def get_bandwidth(self, name):
        # name can be the same as for get_transaction
        return self.bandwidth[name][0]

    def get_response(self, name):
        # name can be the same as for get_transaction
        return self.response[name][0]

    def get_hit_rate(self, name):
        # name can be the same as for get_transaction
        return self.hit_rate[name][0]

    def get_connections(self, name):
        # name can be:
        #   idle_client idle_server total_client total_server
        # Retunrs:
        #   A string.
        return self.connections[name][0]

if __name__ == '__main__':
    # session host defaults to .iafrc.DUT
    cli = status(clictorbase.get_sess())
    st = cli()

    print 'system:up since', st.get_system('up_since')
    print 'transactions:ave_since_restart', st.get_transactions('ave_since_restart')
    print 'bandwidth:ave_last_hour', st.get_bandwidth('ave_last_hour')
    print 'response:ave_last_minute', st.get_response('ave_last_minute')
    print 'hit_rate:max_last_hour', st.get_hit_rate('max_last_hour')
    print 'connections:total_client', st.get_connections('total_client')

    # prints all the status info
    print
    print '-'*75
    print 'ALL COUNTERS'
    print '-'*75
    print st
