#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/antivirusstatus.py#1 $

"""
    antivirustatus ctor
"""
import re

import clictorbase as ccb


class antivirusstatus(ccb.IafCliConfiguratorBase):
    """antivirusstatus"""

    def __call__(self, vendor='sophos', detail_bool=False):

        if detail_bool:
            cmd = 'antivirusstatus detail'
        else:
            vendor = vendor.lower()
            assert vendor in ('sophos', 'mcafee')
            cmd = 'antivirusstatus'
        self.clearbuf()
        self._writeln(cmd)
        self._expect([self._get_prompt(), 'Choose the operation'])
        lines = self.getbuf()

        # returns the string out put if 'antivirusstatus detail' is executed
        if detail_bool:
            return lines

        if self._expectindex == 1:
            self._query_response(vendor)
            # strangeness:  in validator world, sometimes this is needed
            # twice since the ctor inexplicably sends 'antivirusstatus'
            # twice, causing a failure.  Remove this once we figure out
            # why this is happening.
            try:
                lines = self._wait_for_prompt()
            except ccb.IafUnknownOptionError:
                lines = self._wait_for_prompt()

        if vendor == 'sophos':
            return antivirusstatusSophos(lines)
        elif vendor == 'mcafee':
            return antivirusstatusMcAfee(lines)


class antivirusstatusInfo:
    def __init__(self):
        # skip 1st (antivirusstatus) and last (prompt) lines
        self.vals = {}

    def _parse_lines(self, lines):
        for line in lines:
            line = line.strip()
            if re.search('^\s*$', line): continue  # skip blank lines
            for s in self.av_map.keys():
                if line.find(s) >= 0:
                    name = self.av_map[s]
                    val = line[len(s):].strip()
                    # set avs key/value
                    self.vals[name] = val
                    break
            else:
                print 'antivirusstatus(): unexpected line[', line, ']'

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
                self.av_map.iteritems()))


class antivirusstatusSophos(antivirusstatusInfo):
    av_map = {
        'SAV Engine Version': 'sav_engine_version',
        'IDE Serial': 'ide_serial',
        'Last Engine Update': 'last_engine_update',
        'Last IDE Update': 'last_ide_update',
        'Last Update Attempt': 'last_update_attempt',
        'Last Update Success': 'last_update_success',
    }

    def __init__(self, raw):
        antivirusstatusInfo.__init__(self)
        for val in self.av_map.values():
            self.vals[val] = None

        if raw.find('Anti-Virus is not enabled') > 0:
            return

        # skip 1st (antivirusstatus) and last (prompt) lines
        self._parse_lines(raw.split('\n')[2:-1])


class antivirusstatusMcAfee(antivirusstatusInfo):
    av_map = {
        'McAfee DATs': 'mcafee_dat_files',
        'McAfee Engine': 'mcafee_engine_version',
    }

    def __init__(self, raw):
        antivirusstatusInfo.__init__(self)
        for val in self.av_map.values():
            self.vals[val] = None

        if raw.find('Anti-Virus is not enabled') > 0:
            return

        # skip 1st (antivirusstatus) and last (prompt) lines
        self._parse_lines(raw.split('\n')[3:-1])


if __name__ == '__main__':
    # if cli_sess is already defined, we have a CLI session object from
    # the validator we can use; if not, we must create one
    try:
        cli_sess
    except NameError:
        cli_sess = ccb.get_sess()

    avs = antivirusstatus(cli_sess)
    print avs(vendor='sophos')
    print avs(vendor='mcafee')
    print avs(vendor='sophos').sav_engine_version
