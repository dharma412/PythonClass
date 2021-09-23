#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/graymailstatus.py#1 $
# $DateTime: 2019/03/22 01:36:06 $
# $Author: aminath $

import clictorbase
import re
import logging


class graymailstatus(clictorbase.IafCliConfiguratorBase):
    def __init__(self, sess):
        self._gm_map = {
            'Graymail Library': 'graymail_library',
            'Graymail Tools': 'graymail_tools'
        }
        self._dict = {}
        clictorbase.IafCliConfiguratorBase.__init__(self, sess)

    def __call__(self):
        self.clearbuf()
        self._writeln('graymailstatus')
        self._wait_for_prompt()
        self._gm_status_output = self.getbuf()
        return self

    def _parse_output(self):
        self._debug(self._gm_status_output)
        graymail_engine_version = self._gm_status_output
        logging.info("Graymail Engine Version: %s", graymail_engine_version)
        lines = self._gm_status_output.split('\n')[3:-1]
        for line in lines:
            line = line.strip()
            if re.search('^\s*$', line):
                continue  # skip blank lines
            for key in self._gm_map.keys():
                if line.find(key) >= 0:
                    name = self._gm_map[key]
                    val = line[len(key):].strip()
                    match = re.match(r'(\S+)\s+(.*)', val, re.I)
                    self._dict[name] = {}
                    self._dict[name]['version'] = match.groups()[0]
                    self._dict[name]['update_date'] = match.groups()[1]

    def status(self):
        if self._gm_status_output.find('This feature is not enabled') > 0:
            self._warn('"Graymail feature is __NOT__ enabled"')
            return

        self._parse_output()
        return self._dict
