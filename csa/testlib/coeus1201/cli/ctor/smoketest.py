#!/usr/bin/env python
# $Id: //prod/main/sarf_centos/testlib/coeus1201/cli/ctor/smoketest.py#1 $
import clictorbase
from sal.exceptions import TimeoutError

no_action_cmds = [
    "clear",
    "commit",
    "last",
    "status",
    "version",
    "who",
    "whoami"
]

ctrl_c_cmds = [
    "help",
    "settime",
    "mailconfig",
    "ping",
    "rollovernow",
    "showconfig",
    "supportrequest",
    "telnet",
    "traceroute",
    "passwd"
]

new_line_cmds = [
    "dnsflush",
    "featurekey",
    "grep",
    "nslookup",
    "tail",
    "techsupport",
    "alertconfig",
    "certconfig",
    "dnsconfig",
    "etherconfig",
    "interfaceconfig",
    "intrelay",
    "logconfig",
    "ntpconfig",
    "routeconfig",
    "setgateway",
    "sethostname",
    "settz",
    "snmpconfig",
    "sshconfig",
    "upgradeconfig",
    "userconfig",
    "proxyconfig"
]

class smoketest(clictorbase.IafCliConfiguratorBase):
    def __call__(self):
        for cmd in no_action_cmds:
            self._writeln(cmd)
            self._wait_for_prompt()
        for cmd in ctrl_c_cmds:
            self._writeln(cmd)
            # Some cmds have subprompts, some don't.
            # For the ones that do, we can't send the
            # interrupt too early...
            try:
                self._query()
            except TimeoutError:
                pass
            self.interrupt()
            self._wait_for_prompt()
        for cmd in new_line_cmds:
            self._writeln(cmd)
            self._writeln('')
            self._wait_for_prompt()
        return "If we made it here, CLI smoke test passes!"

if __name__ == '__main__':
    sess = clictorbase.get_sess()
    st = smoketest(sess)
    # test case
    print st()
