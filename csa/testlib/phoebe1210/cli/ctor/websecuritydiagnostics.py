#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1210/cli/ctor/websecuritydiagnostics.py#1 $ $DateTime: 2019/05/07 03:16:10 $ $Author: bimmanue $

import clictorbase
from clictorbase import REQUIRED, DEFAULT, NO_DEFAULT, IafCliParamMap
from sal.deprecated.expect import REGEX
import re

from sal.containers.yesnodefault import YES, NO


class websecuritydiagnostics(clictorbase.IafCliConfiguratorBase):
    def __init__(self, sess):
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self._writeln('websecuritydiagnostics')
        self._writeln('\n')
        websecuritydiagnostics_output = self._wait_for_prompt()
        return websecuritydiagnosticsInfoObject(websecuritydiagnostics_output)


class websecuritydiagnosticsInfoCounter(list):
    """An object representing a line of output of the websecuritydiagnostics CLI command.
    The line of output is represented by self.pattern.
    self.pattern can contain %s and %d to represent strings and integers.
    The %s and %d will be extracted from the websecuritydiagnostics_output class attribute.
    """
    websecuritydiagnostics_output = ''

    def __init__(self, pattern):
        super(self.__class__, self).__init__(self)
        self.pattern = self.orig_pattern = pattern
        self._parse()

    def _reformat_pattern(self):
        # Should probably translate more special regex characters
        # to handle all cases but this minimal set is sufficient to handle
        # current websecuritydiagnostics output.
        self.pattern = self.pattern.replace('%s', '\s*(.*)')  # %s: string
        self.pattern = self.pattern.replace('%d', '\s*(\S+)\s*')  # %d: integer
        self.pattern = self.pattern.replace('%f', '\s*(\S+)\s*')  # %s: float

    def _parse(self):
        self._reformat_pattern()
        m = re.search(self.pattern, self.websecuritydiagnostics_output)
        if not m:
            return

        self[:] = []  # reinitialize list to an empty list
        for match_value in map(lambda s: s.strip(), m.groups()):
            self.append(match_value)


class websecuritydiagnosticsInfoObject:
    """Object representing the output of the websecuritydiagnostics command.
    websecuritydiagnostics information is broken up and placed into 1 of the 3 categories:

        self.general:    Any info  before the "Response Time" section
        self.responseTime:  Info from "Response Time" section
        self.dnsLookupTime:  Info from "DNSLookup Time" section
    """

    def __init__(self, websecuritydiagnostics_output):
        from sal.containers import cfgholder

        self.general = cfgholder.CfgHolder()
        self.responseTime = cfgholder.CfgHolder()
        self.dnsLookupTime = cfgholder.CfgHolder()

        # Break up websecuritydiagnostics output into component parts.
        # Determine indexes for the sections in the websecuritydiagnostics output
        rt = websecuritydiagnostics_output.find('Response Time')
        dt = websecuritydiagnostics_output.find('DNS Lookup Time')

        general_out = websecuritydiagnostics_output[:rt]
        responseTime_out = websecuritydiagnostics_output[rt:dt]
        dnsLookupTime_out = websecuritydiagnostics_output[dt:]

        configuration = {}

        # General
        configuration[('self.general', general_out)] = {
            'cache_size': 'Cache Size      : %d',
            'cache_hits': 'Cache Hits      : %d'
        }
        # Response Time
        configuration[('self.responseTime', responseTime_out)] = {
            'minimum': 'Minimum    : %s',
            'average': 'Average    : %f',
            'maximum': 'Maximum    : %s'
        }
        # DnsLookup Time
        configuration[('self.dnsLookupTime', dnsLookupTime_out)] = {
            'minimum': 'Minimum    : %s',
            'average': 'Average    : %f',
            'maximum': 'Maximum    : %s'
        }

        for out_tuple, var2patt_dict in configuration.items():
            attribute_holder, partial_websecuritydiagnostics_output = out_tuple
            websecuritydiagnosticsInfoCounter.websecuritydiagnostics_output = partial_websecuritydiagnostics_output
            for var_name, pattern in var2patt_dict.items():
                s = '%s["%s"]=websecuritydiagnosticsInfoCounter(pattern)' % \
                    (attribute_holder, var_name)
                exec (s)

    def __str__(self):
        s = []
        s.append('Cache' + str(self.general))
        s.append('Response Time' + str(self.responseTime))
        s.append('DNS Lookup Time' + str(self.dnsLookupTime))
        return '\n'.join(s)

    def get_general(self, name):
        return self.general[name]

    def get_responseTime(self, name):
        return self.responseTime[name]

    def get_dnsLookupTime(self, name):
        return self.dnsLookupTime[name]


if __name__ == '__main__':
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()
    cli = websecuritydiagnostics(cli_sess)
    st = cli()
    print 'General:Cache Size', st.get_general('cache_size')
    print 'General:Cache Hits', st.get_general('cache_hits')
    print 'Response:Minimum', st.get_responseTime('minimum')
    print 'Response:Minimum', st.get_responseTime('average')
    print 'Response:Minimum', st.get_responseTime('maximum')
    print 'DNSLookup:Minimum', st.get_dnsLookupTime('minimum')
    print 'DNSLookup:Minimum', st.get_dnsLookupTime('average')
    print 'DNSLookup:Minimum', st.get_dnsLookupTime('maximum')
    print st
