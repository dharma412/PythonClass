#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/ctor/traceroute.py#1 $DateTime: $ $Author: aminath $

import re
import clictorbase


class traceroute(clictorbase.IafCliConfiguratorBase):
    def __call__(self, interface='Auto', host=None, options=None):

        if options is not None:
            cmd_string = '%s %s %s' % (self.__class__.__name__, options, host)
            self._writeln(cmd_string)
        else:
            self._writeln(self.__class__.__name__)
            self._query_select_list_item(interface)
            self._query_response(host)

        # attempt to parse and return traceroute data
        raw = self._read_until()
        return TracerouteData(raw)


class TracerouteData:
    def __init__(self, trace):
        self.output = trace

    def __str__(self):
        return self.output

    def parse(self):
        """ Extract (hostname, IP) tuples from traceroute output.
        Returns a list of the tuples.
        """

        # regexp that matches an individual hop in traceroute output
        # When invoking traceroute on the comparison machine, the header
        # line and timeouts ("*") get interleaved with the stuff we're
        # looking for.  (Note that those lines are terminated by "\r\n".)
        traceroute_hop = re.compile(r"""\d+[\s*]+(\S+) \(([0-9.]+)\)""")

        result = []
        for line in self.output.split('\n'):
            match = traceroute_hop.search(line)
            if match:
                result.append((match.group(1).lower(), match.group(2)))
        return result
