#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1362/cli/ctor/hoststatus.py#1 $

"""
IAF 2 CLI command: hoststatus
"""
import deleterecipients, resetcounters

from sal.deprecated.expect import EXACT
from sal.containers import cfgholder
from iafframework import iafcfg

import clictorbase
from clictorbase import IafCliConfiguratorBase, IafCliValueError


class hoststatus(clictorbase.IafCliConfiguratorBase):

    def __init__(self, sess):

        IafCliConfiguratorBase.__init__(self, sess)

        self._set_local_err_dict({
               ('No record of host:', EXACT) : IafCliValueError,})

    def __call__(self, host):

        self._sess.writeln('hoststatus')
        self._query_response(host)
        status_output = self._wait_for_prompt(timeout=180)
        return HostStatusInfoObject(status_output)


class StatusInfoCounter(list):
    "Stolen from status ctor"

    status_output = ''
    def __init__(self, pattern):
        super(self.__class__, self).__init__(self)
        self.pattern = self.orig_pattern = pattern
        self._parse()

    def _reformat_pattern(self):
        self.pattern = self.pattern.replace('%s', '\s*(.*)')# %s: string
        self.pattern = self.pattern.replace('%d', '\s*(\S+)\s*')#%d: integer

    def _parse(self):
        import re
        self._reformat_pattern()
        m = re.search(self.pattern, self.status_output)
        if not m:
            return
        self[:] = [] # reinitialize list to an empty list
        for match_value in map(lambda s: s.strip(), m.groups()):
             self.append(match_value)


class HostStatusInfoObject:
    """Process hoststatus info"""

    def __init__(self, status_output):

        self.system     = cfgholder.CfgHolder()
        self.counters   = cfgholder.CfgHolder()
        self.gauges     = cfgholder.CfgHolder()

        ci = status_output.find('Counters:')
        gi = status_output.find('Gauges:')
        vg = status_output.find('Virtual Gateway(tm) information:')
        ri = status_output.find('SMTP routes for this host:')
        vg = status_output.find('Virtual Gateway(tm) information:')
        system_out      = status_output[:ci]
        counters_out    = status_output[ci:gi]
        gauges_out      = status_output[gi:vg]
        vg_out          = status_output[vg:ri]
        ri_out          = status_output[ri:]
        gauges_out      = status_output[gi:vg]

        self.vg_list = VGStatus(vg_out).vgateway_list
        self.smtp_route_list = SMTPRoute(ri_out).route_list

        self.configuration = {}
        self.configuration[('self.system', system_out)]={
        'status_for':               'Host mail status for: %s',
        'status_as_of':             'Status as of:         %s',
        'up_down':                  'Host up/down:         %s',}
        self.configuration[('self.counters',counters_out)]={
        'soft_bounced_events':        'Soft Bounced Events         %d',
        'completed_recipients':       'Completed Recipients        %d',
        'hard_bounced_recipients':      'Hard Bounced Recipients   %d',
        'dns_hard_bounces':               'DNS Hard Bounces        %d',
        'fivexx_hard_bounces':            '5XX Hard Bounces        %d',
        'filter_hard_bounces':            'Filter Hard Bounces     %d',
        'expired_hard_bounces':           'Expired Hard Bounces    %d',
        'other_hard_bounces':             'Other Hard Bounces      %d',
        'delivered_recipients':         'Delivered Recipients      %d',
        'deleted_recipients':           'Deleted Recipients        %d',}
        self.configuration[('self.gauges',gauges_out)]={
        'active_recipients':            'Active Recipients                %d',
        'unattempted_recipients':       '  Unattempted Recipients         %d',
        'attempted_recipients':         '  Attempted Recipients           %d',
        'current_outbound_connections': '  Current Outbound Connections   %d',
        'pending_outbound_connections': '  Pending Outbound Connections   %d',
        'oldest_message':               'Oldest Message     %s',
        'last_activity':                'Last Activity      %s',}

        for out_tuple, var2patt_dict in self.configuration.items():
            attribute_holder, partial_status_output = out_tuple
            StatusInfoCounter.status_output = partial_status_output
            for var_name, pattern in var2patt_dict.items():
                var2patt_dict[var_name]=StatusInfoCounter(pattern)

    def get_system(self, name):
        """Return system param's value"""
        for key in self.configuration.keys():
            if key[0] == 'self.system':
                return self.configuration[key][name][0]

    def get_counter(self, name):
        """Return counter param's value"""
        for key in self.configuration.keys():
            if key[0] == 'self.counters':
                return self.configuration[key][name][0]

    def get_gauge(self, name):
        """Return gauge param's value"""
        for key in self.configuration.keys():
            if key[0] == 'self.gauges':
                return self.configuration[key][name][0]


class VGEntry:
    def __init__(self, name=None, active_recipients=None):
        """
        attributes values sample:
                             Virtual Gateway(tm) information:
                             ===================================================
        name                 test1.a001.d1.qa17.qa (a001_qa):
                             Host up/down:          up
                             Last Activity          Tue Oct 31 11:59:48 2006 GMT
        act_rcpts            Active Recipients      0
                             ===================================================
        name                 test1.a001.d1.qa17.qa (a003_qa):
                             Host up/down:          up
                             Last Activity          Tue Oct 31 11:59:41 2006 GMT
        act_rcpts            Active Recipients      0
                             ===================================================
        """

        self.name = name
        self.act_rcpts = active_recipients

    def __str__(self):
        res = 'Name: %s, active_recipients: %d' % (self.name,
                                                   self.act_rcpts)

        return res


class VGStatus:
    def __init__(self, ctor_output=None):
        self.output = ctor_output
        self.vgateway_list = []
        self._parse()

    def _parse(self):
        import re

        if not self.output:
            return
        else:
            lines = self.output.split('\r\n')
            line_count = 1
            name = None
            act_rcpt = None
            re_actrcpt_info = re.compile('\s+Active Recipients\s+(\s*(.*))')
            for line in lines[2:]:
                if line.startswith('='):
                    continue
                if line_count == 1:
                    name = line[:-1]
                if line_count == 4:
                    mo = re_actrcpt_info.match(line)
                    if mo:
                        act_rcpt = int(mo.group(1).replace(',',''))
                        self.vgateway_list.append(VGEntry(name, act_rcpt))

                    line_count = 1
                    continue

                line_count +=1


class SMTPRoute:
    def __init__(self, ctor_output=None):
        self.output = ctor_output
        self.route_list = []
        self._parse()

    def _parse(self):
        if not self.output:
            return
        else:
            lines = self.output.split('\r\n')
            for line in lines[1:]:
                if line.find('Ordered') >= 0:
                    return
                self.route_list.append(line.strip())


if __name__ == '__main__':
    import smtpspam

    # Get session
    # session host defaults to .iafrc.DUT
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    # iaf2rc mga hostname
    host = iafcfg.get_hostname()

    # Start spammer
    smtp_spam = smtpspam.SmtpSpam()
    smtp_spam.num_msgs = 100
    if host.find('.eng') > -1:
        smtp_spam.inject_host = host
        smtp_spam.port = 8025
    smtp_spam.rcpt_host_list = host
    smtp_spam.start()
    smtp_spam.wait()

    # Run hoststatus
    hoststat = hoststatus(cli_sess)
    st = hoststat(host=host)

    print "\n--System--"
    print "Host mail status for:           ", st.get_system('status_for')
    print "Status as of:                   ", st.get_system('status_as_of')
    print "Host up/down:                   ", st.get_system('up_down')
    print "\n--Counters--"
    print "Soft Bounced Events             ",\
                                   st.get_counter('soft_bounced_events')
    print "Completed Recipients            ",\
                                   st.get_counter('completed_recipients')
    print "Hard Bounced Recipients         ",\
                                   st.get_counter('hard_bounced_recipients')
    print "DNS Hard Bounces                ", st.get_counter('dns_hard_bounces')
    print "5XX Hard Bounces                ",\
                                   st.get_counter('fivexx_hard_bounces')
    print "Filter Hard Bounces             ",\
                                   st.get_counter('filter_hard_bounces')
    print "Expired Hard Bounces            ",\
                                   st.get_counter('expired_hard_bounces')
    print "Other Hard Bounces              ",\
                                   st.get_counter('other_hard_bounces')
    print "Delivered Recipients            ",\
                                   st.get_counter('delivered_recipients')
    print "Deleted Recipients              ",\
                                   st.get_counter('deleted_recipients')
    print "\n--Gauges--"
    print "Active Recipients               ", st.get_gauge('active_recipients')
    print "Unattempted Recipients          ",\
                                   st.get_gauge('unattempted_recipients')
    print "Attempted Recipients            ",\
                                   st.get_gauge('attempted_recipients')
    print "Current Outbound Connections    ",\
                                   st.get_gauge('current_outbound_connections')
    print "Pending Outbound Connections    ",\
                                   st.get_gauge('pending_outbound_connections')
    print "Oldest Message                  ", st.get_gauge('oldest_message')
    print "Last Activity                   ", st.get_gauge('last_activity')

    # Now that we're done delete any recipients left on the box
    deleterecipients.deleterecipients(cli_sess)()

 # EOF
