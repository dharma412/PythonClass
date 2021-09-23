#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/zeus1350/cli/ctor/licensesmartagentstatus.py#1 $
# $DateTime: 2019/09/18 01:46:35 $
# $Author: sarukakk $

"""
  licensesmartagentstatus ctor
"""
import re
import clictorbase as ccb


class licensesmartagentstatus(ccb.IafCliConfiguratorBase):
    def __call__(self):
        self.clearbuf()
        self._writeln('license_smart_agentstatus')
        self._expect('Smart License Agent')
        return self

    def agent_status(self):
        agent_status = self._read_until()
        self.agent = {
            'Agent Version': {},
            'Last Updated': {},
        }

        lines = agent_status.split('\n')
        for line in lines:
            match = re.match(r'.*?(\d+.\d+.\d+).*', line, re.I)
            if match:
                version = re.search(r'.*?(\d+.\d+.\d+).*', line).group(1)
                update = re.search(r'.*?\d+.\d+.\d+\s+(.*)', line).group(1)
                self.agent['Agent Version'] = version.strip()
                self.agent['Last Updated'] = update.strip()
                break
            else:
                self._debug("Agent Status not displayed")
        return self.agent
