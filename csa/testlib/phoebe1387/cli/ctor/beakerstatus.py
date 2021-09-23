# $Id: //prod/main/sarf_centos/testlib/phoebe1350/cli/ctor/beakerstatus.py#1 $
# $DateTime: 2020/01/17 04:04:23 $
# $Author: aminath $

import clictorbase
import re


class beakerstatus(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self._sess.writeln(self.__class__.__name__)
        return self._parse_beaker_status_output(self._read_until())

    def _parse_beaker_status_output(self, data):
        status_output = data.split("\r\n")[3:-1]
        status = {}
        for line in status_output:
            component, version, last_updated = re.search(r'(.*)\s(\d\S+)\s+(.*)', line).groups()
            status[component.strip()] = {
                    'Version': version,
                    'Last Updated': last_updated
            }
        return status
