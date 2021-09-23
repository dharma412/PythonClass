#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/phoebe1100/cli/ctor/smartagentstatus.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

"""
SARF CLI command: smartlicense
"""
import re
import time
import pprint

import clictorbase as ccb
from clictorbase import REQUIRED, DEFAULT, IafCliError, IafCliParamMap, IafCliConfiguratorBase
from sal.deprecated.expect import REGEX, EXACT
from sal.exceptions import ConfigError
from sal.containers.yesnodefault import YES, NO, is_no


class smartagentstatus(ccb.IafCliConfiguratorBase):
    def __call__(self, smartagent):
        if smartagent == "status":
            self._writeln('smartlicenseagentstatus')
            self._expect(['Last Updated', ], timeout=5)
        else:
            self._writeln('smartlicenseagentupdate')
            self._expect(['Requesting update of Smart License Agent', ], timeout=5)
        return self

    def agent_status(self):
        agent_status = self._read_until(timeout=30)
        self.agent = {
            'Agent Version': {},
            'Last Updated': {},
        }

        # Agent version
        version = re.search(r'([0-9]*[.][0-9]*[.][0-9]*)', agent_status, re.DOTALL | re.MULTILINE).group(1)
        self.agent['Agent Version'] = version.strip()

        # Last updated
        update = re.search(r'[0-9]*[.][0-9]*[.][0-9](.*)', agent_status, re.DOTALL | re.MULTILINE).group(1)
        self.agent['Last Updated'] = update.strip()

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.agent)
        return self.agent
