import re

import clictorbase


class notificationsstatus(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        self._sess.writeln(self.__class__.__name__)
        status_output = self._read_until()
        component, version, last_updated = re.search(
            r'(.*)\s(\d\S+)\s+(.*)', status_output).groups()
        return {
            'Component': component.strip(),
            'Version': version.strip(),
            'Last Updated': last_updated.strip()
        }
