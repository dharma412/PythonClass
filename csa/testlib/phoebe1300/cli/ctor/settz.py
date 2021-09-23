#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1300/cli/ctor/settz.py#1 $

import clictorbase
from sal.exceptions import ConfigError
import string
import re


class settz(clictorbase.IafCliConfiguratorBase):

    def __call__(self, continent=None, zone=None, validate=False):
        self._restart()
        self.tz_map = {
            'Current time zone': 'current_time_zone',
            'Current time zone version': 'current_time_zone_version',
            'Last update made on': 'last_update',
        }
        self.vals = {}
        for val in self.tz_map.values():
            self.vals[val] = None

        if continent:
            self._writeln("settz %s %s" % (continent, zone))

            if validate:
                rsp = self._wait_for_prompt()

                if rsp.find('Invalid') >= 0:
                    raise ConfigError, string.strip(rsp)
            else:
                self._restart()

        else:
            self._writeln("settz")
            self._expect([self._get_prompt(), 'Choose the operation'])
            lines = self.getbuf()
            self._parse_lines(lines.split('\n')[3:-1])
            return self

    def _parse_lines(self, lines):
        for line in lines:
            line = line.strip()
            if re.search('^\s*$', line): continue  # skip blank lines
            for s in self.tz_map.keys():
                if line.find(s) >= 0:
                    name = self.tz_map[s]
                    val = line[len(s):].strip(':')
                    self.vals[name] = val.strip()
                    break

    def __getattr__(self, attr):
        if self.vals.has_key(attr):
            return self.vals[attr]
        else:
            raise AttributeError

    def __getitem__(self, key):
        if self.vals.has_key(key):
            return self.vals[key]
        else:
            raise KeyError

    def __str__(self):
        return '\n'.join(
            map(lambda (key, val): '%s:%s' % (key.ljust(20), self.vals[val]),
                self.tz_map.iteritems()))

    def setup(self, continent=None, country=None, zone=None):
        self._query_response('setup')
        self._query_select_list_item(continent)
        self._query_select_list_item(country)
        self._query_select_list_item(zone)
        self._restart()

    def Print(self):
        # return to the CLI prompt
        self._to_the_top(1)
        self._writeln('settz print')
        result = self._read_until('>', timeout=3)
        return result


if __name__ == '__main__':

    # if cli_sess object is present in namespace, we're using
    # the dev unit test harness, don't get a new one
    # also set valid gateway address to eng env if present, qa if not
    try:
        cli_sess
    except NameError:
        cli_sess = clictorbase.get_sess()

    stz = settz(cli_sess)
    print stz().last_update
    print stz().current_time_zone
    print stz().current_time_zone_version
    print 'positive test case'

    stz("America", "Los_Angeles", True)
    print 'negative test case'

    try:
        stz("America", 99, True)
    except ConfigError, ce:
        print 'Timeout error found, as expected in negative test case'

    stz().setup("America", "United States", "Los_Angeles")
    print 'positive test case'

    try:
        stz().setup("Trial", 2, "Los_Angeles")
    except ConfigError, ce:
        print "error - %s" % (ce,)

    print 'Settz test done!'
