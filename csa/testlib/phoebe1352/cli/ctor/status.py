#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/status.py#1 $
"""
IAF Command Line Interface (CLI)
command: - status
"""

import clictorbase

from common.util.featurekeytool import GenericFeatureKey

class status(clictorbase.IafCliConfiguratorBase):
    def __call__(self, detail_bool=True):

        cmd = 'status'
        if detail_bool:
            cmd = 'status detail'
        # run status CLI command
        self.clearbuf()
        self._writeln(cmd)
        status_output = ''
        self._expect('\n')
        while 1:
            try:
                self._expect(['-Press Any Key For More-', '>'],timeout=10)
                status_output = self.getbuf()
                if self._expectindex != 0:
                    break
                else:
                    self._writeln("\n")
                    continue
            except TimeoutError:
                raise TimeoutError, "Dictionary content not found"
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
        import re
        self._reformat_pattern()
        m = re.search(self.pattern, self.status_output)
        if not m:
            return

        self[:] = [] # reinitialize list to an empty list
        for match_value in map(lambda s: s.strip(), m.groups()):
            self.append(match_value)

class StatusInfoObject:
    """Object representing the output of the status CLI command.
    Status information is broken up and placed into 1 of the 5 categories:

        self.system:    Any info  before the "Counters:" section
        self.counters:  Reset/Uptime/Lifetime counters from "Counters:" section
        self.rate:      1/5/15Min Rates from the "Rates(Events Per Hours):"
        self.gauges:    Numeric data from the "Gauges:" section
        self.features:  Feature Key Info

    Note the name of the object attribute maps very closely to the name
    of the name of the field name displayed by the status command.
    Example:
        messages_received -> 'Messages Received         %d %d %d'
    """
    def __init__(self, status_output):
        from sal.containers import cfgholder


        self.system     = cfgholder.CfgHolder()
        self.counters   = cfgholder.CfgHolder()
        self.rate       = cfgholder.CfgHolder()
        self.gauges     = cfgholder.CfgHolder()
        self.features   = cfgholder.CfgHolder()

        # Break up status output into component parts.
        # Determine indexes for the sections in the status output
        fi = status_output.find('Feature - ')
        ci = status_output.find('Counters:')
        ri = status_output.find('Rates')
        gi = status_output.find('Gauges:')
        if ri == -1: # for no-detailed status, Rate section doesn't exist
            ri = gi
        system_out      = status_output[:fi]
        features_out    = status_output[fi:ci]
        counters_out    = status_output[ci:ri]
        rate_out        = status_output[ri:gi]
        gauges_out      = status_output[gi:]

        configuration = {}

        # SYSTEM
        configuration[('self.system',system_out)]={
        'status_as_of':             'Status as of:                  %s',
        'up_since':                 'Up since:                      %s (%s)',
        'last_counter_reset':       'Last counter reset:            %s',
        'system_status':            'System status:                 %s',
        'oldest_message':           'Oldest Message:                %s',
        }

        # COUNTERS: Reset/Uptime/Lifetime
        configuration[('self.counters',counters_out)]={
        'messages_received':            'Messages Received         %d %d %d',
        'recipients_received':          'Recipients Received       %d %d %d',
        'gen_bounce_recipients':        'Gen. Bounce Recipients    %d %d %d',
        'rejected_recipients':          'Rejected Recipients       %d %d %d',
        'dropped_messages':             'Dropped Messages          %d %d %d',
        'soft_bounced_events':          'Soft Bounced Events       %d %d %d',
        'completed_recipients':         'Completed Recipients      %d %d %d',
        'hard_bounced_recipients':      '  Hard Bounced Recipients %d %d %d',
        'dns_hard_bounces':             '    DNS Hard Bounces      %d %d %d',
        'fivexx_hard_bounces':          '    5XX Hard Bounces      %d %d %d',
        'expired_hard_bounces':         '    Expired Hard Bounces  %d %d %d',
        'filter_hard_bounces':          '    Filter Hard Bounces   %d %d %d',
        'other_hard_bounces':           '    Other Hard Bounces    %d %d %d',
        'delivered_recipients':         '  Delivered Recipients    %d %d %d',
        'deleted_recipients':           '  Deleted Recipients      %d %d %d',
        'global_unsub_hits':            '    Global Unsub. Hits    %d %d %d',
        'domainkeys_signed_msgs':       'DomainKeys Signed Msgs    %d %d %d',
        'mid':                          'Message ID (MID)                %d',
        'icid':                         'Injection Conn. ID (ICID)       %d',
        'dcid':                         'Delivery Conn. ID (DCID)        %d',
        }

        # RATE: 1/5/15 Minutes
        configuration[('self.rate',rate_out)]={
        'messages_received':            'Messages Received         %d %d %d',
        'recipients_received':          'Recipients Received       %d %d %d',
        'soft_bounced_events':          'Soft Bounced Events       %d %d %d',
        'completed_recipients':         'Completed Recipients      %d %d %d',
        'hard_bounced_recipients':      '  Hard Bounced Recipients %d %d %d',
        'hard_boucned_recipients':      '  Hard Bounced Recipients %d %d %d',
        'delivered_recipients':         '  Delivered Recipients    %d %d %d',
        }

        # GAUGES: Current
        configuration[('self.gauges',gauges_out)]={
        'ram_utilization':              'RAM Utilization           %d%%',
        'cpu_utilization_total':        'Overall CPU load average  %d%%',
        'cpu_utilization_mga':          '  MGA                     %d%%',
        'cpu_utilization_case':         '  CASE                    %d%%',
        'cpu_utilization_bm_antispam':  '  Brightmail AntiSpam     %d%%',
        'cpu_utilization_antivirus':    '  AntiVirus               %d%%',
        'disk_io_utilization':          'Disk I/O Utilization      %d%%',
        'resource_conservation':        'Resource Conservation     %d',
        'logging_disk_usage':           'Logging Disk Usage        %d%%',
        'logging_disk_available':       'Logging Disk Available    %s',
        'current_inbound_conn':         'Current Inbound Conn.     %d',
        'current_outbound_conn':        'Current Outbound Conn.    %d',
        'active_recipients':            'Active Recipients         %d',
        'unattempted_recipients':       '  Unattempted Recipients  %d',
        'attempted_recipients':         '  Attempted Recipients    %d',
        'messages_in_work_queue':       'Messages In Work Queue    %d',
        'messages_in_quarantine':       'Messages In Quarantine\s+Policy, Virus and Outbreak  %d',
        'destinations_in_memory':       'Destinations In Memory    %d',
        'kilobytes_used':               'Kilobytes Used            %d',
        'kilobytes_in_quarantine':      'Kilobytes In Quarantine\s+Policy, Virus and Outbreak  %d',
        'kilobytes_free':               'Kilobytes Free            %s',
        }

        for out_tuple, var2patt_dict in configuration.items():
            attribute_holder, partial_status_output = out_tuple
            StatusInfoCounter.status_output = partial_status_output
            for var_name, pattern in var2patt_dict.items():
                s='%s["%s"]=StatusInfoCounter(pattern)'%\
                        (attribute_holder,var_name)
                exec(s)

        # FEATURE KEYS
        for feature_line in features_out.split('\n'):
            if feature_line.find('Feature') < 0:
                continue
            StatusInfoCounter.status_output = feature_line

            # First %s is key name. Second %s is Time Remaining.
            fkey_name, fkey_time = StatusInfoCounter('Feature - %s: %s')

            # fkey_name
            fkey_name = self._parse_fkey_name(fkey_name)
            assert not self.features.get(fkey_name),\
                'fkey_name(%s) already exists!' % fkey_name

            # seconds_remaining
            dut = None
            fk = GenericFeatureKey(dut, None, None)
            seconds_remaining = fk.convert_key_time_seconds(fkey_time)

            self.features[fkey_name] = seconds_remaining

    def _parse_fkey_name(self, fkey_name):
        """This method converts the input fkey_name string
        to a valid python variable name. The new fkey_name will be
        used as the key to a python dictionary.

        Examples of fkey_name and the resulting attribute name:
            'Virus Outbreak Filters'-> virusoutbreakfilters
            'IronPort Anti-Spam'    -> ironportantispam
            'Receiving'             -> receiving
            'Brightmail'            -> brightmail
            'Sophos'                -> sophos
            'Central Mgmt'          -> centralmgmt
        """
        import re

        fkey_name = fkey_name.lower()
        fkey_name = re.sub('\s', '', fkey_name)
        fkey_name = re.sub('\W', '', fkey_name)
        if re.search('^\d',fkey_name):
            fkey_name = '_' + fkey_name
        return fkey_name

    def __str__(self):
        s = []
        s.append('STATUS:'+str(self.system))
        s.append('COUNTERS:'+str(self.counters))
        s.append('RATE:'+str(self.rate))
        s.append('GAUGES:'+str(self.gauges))
        s.append('FEATURES:'+str(self.features))
        return '\n'.join(s)

    def get_system(self, name, idx=0):
        # name can be:
        #   status_as_of up_since last_counter_reset system_status
        #   oldest_message
        #
        # idx:
        #   up_since has 2 values. So idx can be 0 or 1 for this attribute.
        #   idx must be zero for every other 'name'.
        # Returns:
        #   A string.
        assert (name == 'up_since' and idx in (0,1)) or (idx == 0)
        return self.system[name][idx]

    def get_counter(self, name, idx=0):
        # name can be:
        #   messages_received recipients_received gen_bounce_recipients
        #   rejected_recipients dropped_messages soft_bounced_events
        #   completed_recipients hard_bounced_recipients dns_hard_bounces
        #   fivexx_hard_bounces expired_hard_bounces filter_hard_bounces
        #   other_hard_bounces delivered_recipients deleted_recipients
        #   global_unsub_hits domainkeys_signed_msgs mid icid dcid
        # idx can be:
        #   0,1,2, reset, uptime, lifetime. The integers are mapped as follows
        #                                   0:reset,1:uptime,2:lifetime
        # Returns:
        #   A string.
        if str(idx).lower() in ('reset', 'uptime', 'lifetime'):
            idx = {'reset':0,'uptime':1,'lifetime':2}[idx]
        return self.counters[name][idx]

    def get_rate(self, name, idx=0):
        # name can be:
        #   messages_received recipients_received soft_bounced_events
        #   completed_recipients hard_boucned_recipients delivered_recipients
        # idx can be:
        #   0,1,2, 1min, 5min, 15Min.  The integers are mapped as follows
        #                              0:1min, 1:5min, 2:15min
        # Returns:
        #   A string.
        if str(idx).lower() in ('1min', '5min', '15min'):
            idx = {'1min':0,'5min':1,'15min':2}[idx]
        return self.rate[name][idx]

    def get_gauge(self, name):
        # name can be:
        #   ram_utilization cpu_utilization_total cpu_utilization_mga
        #   cpu_utilization_case cpu_utilization_bm_antispam
        #   cpu_utilization_antivirus disk_io_utilization resource_conservation
        #   logging_disk_usage logging_disk_available current_inbound_conn
        #   current_outbound_conn active_recipients unattempted_recipients
        #   attempted_recipients messages_in_work_queue messages_in_quarantine
        #   destinations_in_memory kilobytes_used kilobytes_in_quarantine
        #   kilobytes_free
        # Returns:
        #   A string.
        idx = 0
        return self.gauges[name][idx]

    def get_feature(self, name):
        # name can be:
        #   virusoutbreakfilters ironportantispam receiving brightmail
        #   sophos centralmgmt
        # Other fkey names are valid and accepted they are just not listed here.
        # Look at _parse_fkey_name() to see how feature key names are generated
        #
        # Returns:
        #   An integer. Seconds remaining.
        fk_name = self._parse_fkey_name(name)
        seconds_remaining = self.features[fk_name]
        return seconds_remaining

if __name__ == '__main__':
    # session host defaults to .iafrc.DUT
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    cli = status(cli_sess)
    st = cli()
    print 'system:as of:', st.get_system('status_as_of')
    print 'system:system status:', st.get_system('system_status')
    print 'counter:messages received:', st.get_counter('messages_received')
    print 'rate:messages received:', st.get_rate('messages_received')
    print 'gauge:ram utilization:', st.get_gauge('ram_utilization')
    #receiving_feature_name = 'receiving' # old name
    receiving_feature_name = 'incomingmailhandling' # new name in 4.7
    print 'receiving key duration(in seconds):',\
                                    st.get_feature(receiving_feature_name)

    print 'rate:msgs received[ 1min]',st.get_rate('messages_received', '1min')
    print 'rate:msgs received[ 5min]',st.get_rate('messages_received', '5min')
    print 'rate:msgs received[15min]',st.get_rate('messages_received', '15min')

    # prints all the status info
    print
    print '-'*75
    print 'ALL COUNTERS'
    print '-'*75
    print st
