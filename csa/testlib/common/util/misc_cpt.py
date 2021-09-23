import re
from common.util.utilcommon import UtilCommon


class MiscCpt(UtilCommon):
    def get_keyword_names(self):
        return [
            'uptime_seconds',
        ]

    def uptime_seconds(self):
        stout = self._shell.send_cmd("cli status")
        (days, hrs, mins, secs) = (0, 0, 0, 0)
        m = re.search("Up since:.*\((\\d+d)?\\s*(\\d+h)?\\s*(\\d+m)?\\s*(\\d+s)\)", stout)
        if m:
            if m.group(1) is not None:
                days = int(m.group(1)[0:-1])
            if m.group(2) is not None:
                hrs = int(m.group(2)[0:-1])
            if m.group(3) is not None:
                mins = int(m.group(3)[0:-1])
            if m.group(4) is not None:
                secs = int(m.group(4)[0:-1])

        return (days * 86400) + (hrs * 3600) + (mins * 60) + secs
